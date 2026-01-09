#!/bin/bash
# Home Assistant Automation Tester
# Trigger automations and monitor their execution

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check environment
check_env() {
    if [[ -z "$HASS_SERVER" || -z "$HASS_TOKEN" ]]; then
        echo -e "${RED}Error: HASS_SERVER and HASS_TOKEN must be set${NC}"
        echo "Run: source ~/.hass-cli.env"
        exit 1
    fi
}

# List automations
list_automations() {
    echo -e "${BLUE}Available Automations:${NC}"
    echo ""

    curl -s -H "Authorization: Bearer $HASS_TOKEN" \
        "$HASS_SERVER/api/states" | \
        jq -r '.[] | select(.entity_id | startswith("automation.")) | "\(.entity_id) - \(.attributes.friendly_name // "No name") [\(.state)]"' | \
        sort
}

# Trigger automation
trigger_automation() {
    local entity_id="$1"
    local skip_condition="${2:-false}"

    if [[ -z "$entity_id" ]]; then
        echo -e "${RED}Error: No automation specified${NC}"
        echo "Usage: $0 trigger <automation.entity_id> [--skip-conditions]"
        return 1
    fi

    # Add automation. prefix if not present
    if [[ ! "$entity_id" =~ ^automation\. ]]; then
        entity_id="automation.$entity_id"
    fi

    echo -e "${BLUE}Triggering: $entity_id${NC}"
    echo "Skip conditions: $skip_condition"
    echo ""

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"entity_id\": \"$entity_id\", \"skip_condition\": $skip_condition}" \
        "$HASS_SERVER/api/services/automation/trigger")

    if [[ -n "$response" && "$response" != "[]" ]]; then
        echo -e "${GREEN}Automation triggered successfully${NC}"
        echo "Response: $response"
    else
        echo -e "${YELLOW}Automation triggered (no response data)${NC}"
    fi
}

# Get automation info
get_automation_info() {
    local entity_id="$1"

    if [[ -z "$entity_id" ]]; then
        echo -e "${RED}Error: No automation specified${NC}"
        return 1
    fi

    if [[ ! "$entity_id" =~ ^automation\. ]]; then
        entity_id="automation.$entity_id"
    fi

    echo -e "${BLUE}Automation Info: $entity_id${NC}"
    echo ""

    curl -s -H "Authorization: Bearer $HASS_TOKEN" \
        "$HASS_SERVER/api/states/$entity_id" | \
        jq '.'
}

# Enable/disable automation
toggle_automation() {
    local entity_id="$1"
    local action="$2"

    if [[ -z "$entity_id" ]]; then
        echo -e "${RED}Error: No automation specified${NC}"
        return 1
    fi

    if [[ ! "$entity_id" =~ ^automation\. ]]; then
        entity_id="automation.$entity_id"
    fi

    case "$action" in
        enable|on)
            echo "Enabling $entity_id..."
            curl -s -X POST \
                -H "Authorization: Bearer $HASS_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"entity_id\": \"$entity_id\"}" \
                "$HASS_SERVER/api/services/automation/turn_on" > /dev/null
            echo -e "${GREEN}Automation enabled${NC}"
            ;;
        disable|off)
            echo "Disabling $entity_id..."
            curl -s -X POST \
                -H "Authorization: Bearer $HASS_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"entity_id\": \"$entity_id\"}" \
                "$HASS_SERVER/api/services/automation/turn_off" > /dev/null
            echo -e "${YELLOW}Automation disabled${NC}"
            ;;
        *)
            echo "Usage: $0 toggle <automation.entity_id> <enable|disable>"
            return 1
            ;;
    esac
}

# Watch automation events
watch_events() {
    echo -e "${BLUE}Watching automation events (Ctrl+C to stop)...${NC}"
    echo ""

    if command -v hass-cli &> /dev/null; then
        hass-cli event watch automation_triggered
    else
        echo -e "${YELLOW}hass-cli not installed. Install it for real-time event watching.${NC}"
        echo "Alternative: Check Developer Tools > Events in Home Assistant UI"
    fi
}

# Show help
show_help() {
    echo "Home Assistant Automation Tester"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  list                          List all automations"
    echo "  trigger <entity_id>           Trigger an automation"
    echo "    --skip-conditions           Skip condition checks"
    echo "  info <entity_id>              Get automation details"
    echo "  toggle <entity_id> <on|off>   Enable/disable automation"
    echo "  watch                         Watch automation events"
    echo "  help                          Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 trigger motion_lights_living_room"
    echo "  $0 trigger automation.motion_lights --skip-conditions"
    echo "  $0 info motion_lights_living_room"
    echo "  $0 toggle motion_lights_living_room off"
    echo ""
    echo "Environment variables:"
    echo "  HASS_SERVER  Home Assistant URL"
    echo "  HASS_TOKEN   Long-lived access token"
}

# Main
main() {
    case "${1:-}" in
        list)
            check_env
            list_automations
            ;;
        trigger)
            check_env
            skip="false"
            if [[ "$3" == "--skip-conditions" ]]; then
                skip="true"
            fi
            trigger_automation "$2" "$skip"
            ;;
        info)
            check_env
            get_automation_info "$2"
            ;;
        toggle)
            check_env
            toggle_automation "$2" "$3"
            ;;
        watch)
            check_env
            watch_events
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
