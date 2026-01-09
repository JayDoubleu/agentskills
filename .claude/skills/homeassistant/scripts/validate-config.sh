#!/bin/bash
# Home Assistant Configuration Validator
# Validates configuration before restart to prevent downtime

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check environment
check_env() {
    if [[ -z "$HASS_SERVER" || -z "$HASS_TOKEN" ]]; then
        echo -e "${RED}Error: HASS_SERVER and HASS_TOKEN must be set${NC}"
        echo "Run: source ~/.hass-cli.env"
        exit 1
    fi
}

# Validate via REST API
validate_rest_api() {
    echo "Validating configuration via REST API..."

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -H "Content-Type: application/json" \
        "$HASS_SERVER/api/config/core/check_config")

    result=$(echo "$response" | jq -r '.result // "unknown"')
    errors=$(echo "$response" | jq -r '.errors // "none"')

    if [[ "$result" == "valid" ]]; then
        echo -e "${GREEN}Configuration is valid${NC}"
        return 0
    else
        echo -e "${RED}Configuration errors found:${NC}"
        echo "$errors"
        return 1
    fi
}

# Validate via hass-cli
validate_hass_cli() {
    if command -v hass-cli &> /dev/null; then
        echo "Validating via hass-cli..."
        hass-cli config check
    fi
}

# Check YAML syntax locally
check_yaml_syntax() {
    local file="$1"

    if [[ -z "$file" ]]; then
        echo "Usage: $0 --yaml <file>"
        return 1
    fi

    if ! [[ -f "$file" ]]; then
        echo -e "${RED}File not found: $file${NC}"
        return 1
    fi

    echo "Checking YAML syntax: $file"

    # Use Python to validate YAML
    if command -v python3 &> /dev/null; then
        python3 -c "
import yaml
import sys

try:
    with open('$file', 'r') as f:
        yaml.safe_load(f)
    print('YAML syntax is valid')
    sys.exit(0)
except yaml.YAMLError as e:
    print(f'YAML error: {e}')
    sys.exit(1)
"
    else
        echo -e "${YELLOW}Python not available for local YAML validation${NC}"
    fi
}

# Main
main() {
    case "${1:-}" in
        --yaml)
            check_yaml_syntax "$2"
            ;;
        --local)
            check_yaml_syntax "$2"
            ;;
        --help|-h)
            echo "Home Assistant Configuration Validator"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  (none)       Validate via REST API (requires HASS_SERVER, HASS_TOKEN)"
            echo "  --yaml FILE  Check YAML syntax locally"
            echo "  --help       Show this help"
            echo ""
            echo "Environment variables:"
            echo "  HASS_SERVER  Home Assistant URL (e.g., http://homeassistant.local:8123)"
            echo "  HASS_TOKEN   Long-lived access token"
            ;;
        *)
            check_env
            validate_rest_api
            ;;
    esac
}

main "$@"
