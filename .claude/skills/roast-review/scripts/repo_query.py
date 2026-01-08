#!/usr/bin/env python3
"""
Simple repo analysis tool using repomix and Google Gemini.

This script packs a repository using repomix and sends it to Google Gemini
for context-aware analysis and question answering.

Usage:
    python repo_query.py "your question about the codebase"
    python repo_query.py --repo /path/to/repo "your question"

Requirements:
    - repomix CLI: npm install -g repomix
    - google-genai: pip install google-genai
    - GEMINI_API_KEY environment variable set
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    from google import genai
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)


SUPPORTED_MODELS = [
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
]

DEFAULT_MODEL = "gemini-2.5-flash"


class Spinner:
    """Simple spinner to show activity during long operations."""

    def __init__(self, message: str):
        self.message = message
        self.running = False
        self.thread = None
        self.start_time = None

    def _spin(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self.running:
            elapsed = time.time() - self.start_time
            sys.stdout.write(f"\r{chars[i]} {self.message} ({elapsed:.1f}s)")
            sys.stdout.flush()
            i = (i + 1) % len(chars)
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def stop(self, final_message: str = None):
        self.running = False
        if self.thread:
            self.thread.join()
        elapsed = time.time() - self.start_time
        if final_message:
            sys.stdout.write(f"\r✓ {final_message} ({elapsed:.1f}s)\n")
        else:
            sys.stdout.write(f"\r✓ {self.message} ({elapsed:.1f}s)\n")
        sys.stdout.flush()


SYSTEM_PROMPT = """You are an expert software developer analyzing a codebase.
Your task is to answer questions about the repository content provided below.

Guidelines:
- Provide accurate, detailed answers based on the actual code
- Reference specific files and line numbers when relevant
- If you're unsure about something, say so
- Be concise but thorough"""


def get_repomix_command(verbose: bool = True) -> tuple[list[str] | None, str]:
    """Find available repomix command (direct or via npx).

    Returns (command, error_message) - command is None if not found.
    """
    # Try direct repomix first
    if shutil.which("repomix"):
        return ["repomix"], ""

    # Fall back to npx
    if not shutil.which("npx"):
        return (
            None,
            "Node.js/npm not found. Install Node.js first, then run: npm install -g repomix",
        )

    # npx repomix (first run may download packages)
    if verbose:
        spinner = Spinner("Checking npx repomix (first run may download packages)")
        spinner.start()
    try:
        subprocess.run(
            ["npx", "--yes", "repomix", "--version"],
            capture_output=True,
            check=True,
            timeout=120,
        )
        if verbose:
            spinner.stop("Found npx repomix")
        return ["npx", "--yes", "repomix"], ""
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        if verbose:
            spinner.stop("npx repomix failed")
        return None, f"npx repomix failed: {e}"


def get_repomix_cache_path(repo_path: Path) -> Path:
    """Get deterministic cache file path for a repo based on its absolute path."""
    path_hash = hashlib.md5(str(repo_path).encode()).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"repomix-{path_hash}.txt"


def get_file_age_str(file_path: Path) -> str:
    """Get human-readable file age."""
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    age = datetime.now() - mtime
    if age.total_seconds() < 60:
        return f"{int(age.total_seconds())}s ago"
    elif age.total_seconds() < 3600:
        return f"{int(age.total_seconds() / 60)}m ago"
    elif age.total_seconds() < 86400:
        return f"{int(age.total_seconds() / 3600)}h ago"
    else:
        return f"{int(age.total_seconds() / 86400)}d ago"


def pack_repository(
    repo_path: Path, repomix_cmd: list[str], use_cache: bool = True
) -> tuple[str, Path]:
    """Pack the repository using repomix and return the content and cache path.

    Returns (content, cache_file_path) tuple.
    """
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    cache_file = get_repomix_cache_path(repo_path)

    # Check if cached file exists and use_cache is True
    if use_cache and cache_file.exists():
        with open(cache_file, "r") as f:
            content = f.read()
        return content, cache_file

    # Generate new repomix file
    try:
        subprocess.run(
            [
                *repomix_cmd,
                "--output",
                str(cache_file),
                "--style",
                "plain",
                str(repo_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        with open(cache_file, "r") as f:
            content = f.read()

        return content, cache_file

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"repomix failed: {e.stderr}")


class QueryResult:
    """Result from a Gemini query including text and token usage."""

    def __init__(self, text: str, usage_metadata):
        self.text = text
        self.prompt_tokens = getattr(usage_metadata, "prompt_token_count", 0)
        self.output_tokens = getattr(usage_metadata, "candidates_token_count", 0)
        self.total_tokens = getattr(usage_metadata, "total_token_count", 0)


# Pricing per 1M tokens (as of Jan 2026)
MODEL_PRICING = {
    "gemini-3-pro-preview": {"input": 2.00, "output": 12.00},
    "gemini-3-flash-preview": {"input": 0.15, "output": 0.60},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "gemini-flash-latest": {"input": 0.15, "output": 0.60},
    "gemini-flash-lite-latest": {"input": 0.10, "output": 0.40},
}


def query_gemini(
    repo_content: str, query: str, model_name: str = "gemini-2.5-flash"
) -> QueryResult:
    """Send the repository content and query to Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    full_prompt = f"""{SYSTEM_PROMPT}

## Repository Content

{repo_content}

## User Query

{query}

Please answer the query based on the repository content above."""

    response = client.models.generate_content(
        model=model_name,
        contents=full_prompt,
    )
    return QueryResult(response.text, response.usage_metadata)


def main():
    parser = argparse.ArgumentParser(
        description="Query a repository using AI (repomix + Gemini)"
    )
    parser.add_argument(
        "query", nargs="?", help="The question to ask about the repository"
    )
    parser.add_argument(
        "--repo",
        "-r",
        default=".",
        help="Path to the repository (default: current directory)",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        choices=SUPPORTED_MODELS,
        help=f"Gemini model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--list-models", action="store_true", help="List supported models and exit"
    )
    parser.add_argument(
        "--output", "-o", help="Save response to file (useful for long outputs)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Force regeneration of repomix file (ignore cached version)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode - minimal output, no spinners (for automation/agents)",
    )

    args = parser.parse_args()

    if args.list_models:
        print("Supported models:")
        for model in SUPPORTED_MODELS:
            marker = " (default)" if model == DEFAULT_MODEL else ""
            print(f"  - {model}{marker}")
        sys.exit(0)

    if not args.query:
        parser.error("query is required")

    quiet = args.quiet

    if not quiet:
        print("Checking for repomix...")
    repomix_cmd, error_msg = get_repomix_command(verbose=not quiet)
    if not repomix_cmd:
        print(f"Error: {error_msg}")
        sys.exit(1)
    if not quiet:
        print(f"✓ Found repomix: {' '.join(repomix_cmd)}")

    repo_path = Path(args.repo).resolve()
    use_cache = not args.no_cache

    try:
        # Check if we'll use cache
        cache_file = get_repomix_cache_path(repo_path)
        cache_exists = cache_file.exists() and use_cache

        if cache_exists:
            # Using cached file
            file_size = cache_file.stat().st_size
            file_age = get_file_age_str(cache_file)
            if not quiet:
                print(f"✓ Using cached repomix ({file_age}, {file_size:,} bytes)")
            print(f"Repomix cache: {cache_file}")
            repo_content, _ = pack_repository(repo_path, repomix_cmd, use_cache=True)
        else:
            # Generate new repomix
            if not quiet:
                spinner = Spinner(f"Packing repository: {repo_path}")
                spinner.start()
            repo_content, cache_file = pack_repository(
                repo_path, repomix_cmd, use_cache=False
            )
            file_size = cache_file.stat().st_size
            if not quiet:
                spinner.stop(f"Repository packed ({len(repo_content):,} chars)")
            print(f"Repomix file: {cache_file}")

        # Estimate tokens (rough: ~4 chars per token)
        estimated_tokens = len(repo_content) // 4
        if not quiet:
            print(f"  Estimated tokens: ~{estimated_tokens:,}")

        # Query Gemini
        if not quiet:
            spinner = Spinner(
                f"Sending to {args.model} (this may take a while for large repos)"
            )
            spinner.start()
        result = query_gemini(repo_content, args.query, args.model)
        if not quiet:
            spinner.stop(f"Response received from {args.model}")

        # Calculate cost
        pricing = MODEL_PRICING.get(args.model, {"input": 0, "output": 0})
        input_cost = result.prompt_tokens * pricing["input"] / 1_000_000
        output_cost = result.output_tokens * pricing["output"] / 1_000_000
        total_cost = input_cost + output_cost

        # Output token usage (always shown, even in quiet mode for skill parsing)
        print(f"Token usage: {result.prompt_tokens:,} input, {result.output_tokens:,} output, {result.total_tokens:,} total")
        print(f"Estimated cost: ${total_cost:.4f} ({args.model})")

        # Output response
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                f.write(result.text)
            print(f"Response saved: {output_path.resolve()}")
            if not quiet:
                print(f"  Length: {len(result.text):,} characters")
        else:
            if not quiet:
                print("\n" + "=" * 60)
                print("Response:")
                print("=" * 60 + "\n")
            print(result.text)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
