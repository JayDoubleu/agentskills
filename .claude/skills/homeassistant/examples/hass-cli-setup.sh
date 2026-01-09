#!/bin/bash
# Home Assistant CLI Setup Script
# This script configures hass-cli for remote Home Assistant access

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Home Assistant CLI Setup${NC}"
echo "========================="
echo ""

# Check if hass-cli is installed
if ! command -v hass-cli &> /dev/null; then
    echo -e "${YELLOW}hass-cli is not installed.${NC}"
    echo ""
    echo "Install options:"
    echo "  Fedora/RHEL: sudo dnf install homeassistant-cli"
    echo "  macOS:       brew install homeassistant-cli"
    echo "  pip:         pip install homeassistant-cli"
    echo ""
    read -p "Would you like to install via pip? (y/n): " install_choice
    if [[ "$install_choice" == "y" || "$install_choice" == "Y" ]]; then
        pip install homeassistant-cli
    else
        echo "Please install hass-cli and run this script again."
        exit 1
    fi
fi

echo -e "${GREEN}hass-cli is installed.${NC}"
echo ""

# Get Home Assistant server URL
echo "Enter your Home Assistant server URL"
echo "Example: http://homeassistant.local:8123 or http://192.168.1.100:8123"
read -p "Server URL: " HASS_SERVER

# Validate URL format
if [[ ! "$HASS_SERVER" =~ ^https?:// ]]; then
    HASS_SERVER="http://$HASS_SERVER"
fi

# Remove trailing slash
HASS_SERVER="${HASS_SERVER%/}"

echo ""
echo "Enter your Long-Lived Access Token"
echo "To create one: Home Assistant UI > Profile > Long-Lived Access Tokens > Create Token"
read -p "Token: " HASS_TOKEN

# Test connection
echo ""
echo "Testing connection..."
if HASS_SERVER="$HASS_SERVER" HASS_TOKEN="$HASS_TOKEN" hass-cli info &> /dev/null; then
    echo -e "${GREEN}Connection successful!${NC}"
else
    echo -e "${RED}Connection failed. Please check your server URL and token.${NC}"
    exit 1
fi

# Create environment file
ENV_FILE="$HOME/.hass-cli.env"
echo ""
echo "Saving configuration to $ENV_FILE"

cat > "$ENV_FILE" << EOF
# Home Assistant CLI Configuration
# Source this file: source ~/.hass-cli.env

export HASS_SERVER="$HASS_SERVER"
export HASS_TOKEN="$HASS_TOKEN"
EOF

chmod 600 "$ENV_FILE"

# Add to shell config
echo ""
echo "Add the following line to your shell config (~/.bashrc or ~/.zshrc):"
echo ""
echo -e "${YELLOW}source ~/.hass-cli.env${NC}"
echo ""

read -p "Add to ~/.zshrc automatically? (y/n): " add_choice
if [[ "$add_choice" == "y" || "$add_choice" == "Y" ]]; then
    if ! grep -q "source ~/.hass-cli.env" ~/.zshrc 2>/dev/null; then
        echo "" >> ~/.zshrc
        echo "# Home Assistant CLI" >> ~/.zshrc
        echo "source ~/.hass-cli.env" >> ~/.zshrc
        echo -e "${GREEN}Added to ~/.zshrc${NC}"
    else
        echo "Already in ~/.zshrc"
    fi
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Quick test commands:"
echo "  hass-cli info              - Get Home Assistant info"
echo "  hass-cli state list        - List all entities"
echo "  hass-cli service list      - List available services"
echo "  hass-cli event watch       - Watch events in real-time"
