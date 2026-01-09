#!/bin/bash
# Home Assistant Backup and Restore Helper
# Create, list, and restore backups via REST API

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

# Create backup
create_backup() {
    local name="${1:-backup_$(date +%Y%m%d_%H%M%S)}"

    echo -e "${BLUE}Creating backup: $name${NC}"

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$name\"}" \
        "$HASS_SERVER/api/services/backup/create")

    if [[ "$response" == "[]" || -n "$response" ]]; then
        echo -e "${GREEN}Backup creation initiated${NC}"
        echo "Note: Backup creation runs in background. Use 'list' to check status."
    else
        echo -e "${RED}Failed to create backup${NC}"
        echo "$response"
        return 1
    fi
}

# List backups (requires Supervisor)
list_backups_supervisor() {
    echo -e "${BLUE}Listing backups...${NC}"
    echo ""

    # Try supervisor API
    response=$(curl -s \
        -H "Authorization: Bearer $HASS_TOKEN" \
        "$HASS_SERVER/api/hassio/backups" 2>/dev/null)

    if [[ -n "$response" && "$response" != *"error"* ]]; then
        echo "$response" | jq -r '.data.backups[] | "[\(.slug)] \(.name) - \(.date) (\(.size // "unknown") MB)"' 2>/dev/null || \
        echo "$response" | jq '.'
    else
        echo -e "${YELLOW}Could not list backups via Supervisor API${NC}"
        echo "This feature requires Home Assistant OS or Supervised installation."
        echo ""
        echo "Alternative methods:"
        echo "  - Use 'ha backups list' via SSH on the device"
        echo "  - Check Settings > System > Backups in the UI"
    fi
}

# Download backup
download_backup() {
    local slug="$1"
    local output="${2:-backup_$slug.tar}"

    if [[ -z "$slug" ]]; then
        echo -e "${RED}Error: No backup slug specified${NC}"
        echo "Usage: $0 download <slug> [output_file]"
        return 1
    fi

    echo -e "${BLUE}Downloading backup: $slug${NC}"

    curl -s \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -o "$output" \
        "$HASS_SERVER/api/hassio/backups/$slug/download"

    if [[ -f "$output" && -s "$output" ]]; then
        echo -e "${GREEN}Backup downloaded: $output${NC}"
        ls -lh "$output"
    else
        echo -e "${RED}Failed to download backup${NC}"
        rm -f "$output"
        return 1
    fi
}

# Upload backup
upload_backup() {
    local file="$1"

    if [[ -z "$file" ]]; then
        echo -e "${RED}Error: No backup file specified${NC}"
        echo "Usage: $0 upload <backup_file.tar>"
        return 1
    fi

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}File not found: $file${NC}"
        return 1
    fi

    echo -e "${BLUE}Uploading backup: $file${NC}"

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -F "file=@$file" \
        "$HASS_SERVER/api/hassio/backups/new/upload")

    if [[ "$response" == *"slug"* ]]; then
        echo -e "${GREEN}Backup uploaded successfully${NC}"
        echo "$response" | jq '.'
    else
        echo -e "${RED}Failed to upload backup${NC}"
        echo "$response"
        return 1
    fi
}

# Restore backup
restore_backup() {
    local slug="$1"
    local components="${2:-full}"

    if [[ -z "$slug" ]]; then
        echo -e "${RED}Error: No backup slug specified${NC}"
        echo "Usage: $0 restore <slug> [full|homeassistant|addons]"
        return 1
    fi

    echo -e "${YELLOW}WARNING: Restoring a backup will restart Home Assistant${NC}"
    read -p "Continue with restore of '$slug'? (y/N): " confirm

    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Restore cancelled"
        return 0
    fi

    echo -e "${BLUE}Restoring backup: $slug${NC}"

    case "$components" in
        full)
            data='{"homeassistant": true, "addons": true}'
            ;;
        homeassistant)
            data='{"homeassistant": true}'
            ;;
        addons)
            data='{"addons": true}'
            ;;
        *)
            data='{"homeassistant": true, "addons": true}'
            ;;
    esac

    response=$(curl -s -X POST \
        -H "Authorization: Bearer $HASS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$data" \
        "$HASS_SERVER/api/hassio/backups/$slug/restore/full")

    if [[ "$response" == *"result"*"ok"* ]]; then
        echo -e "${GREEN}Restore initiated${NC}"
        echo "Home Assistant will restart. Please wait..."
    else
        echo -e "${RED}Failed to initiate restore${NC}"
        echo "$response"
        return 1
    fi
}

# Get backup info
backup_info() {
    local slug="$1"

    if [[ -z "$slug" ]]; then
        echo -e "${RED}Error: No backup slug specified${NC}"
        return 1
    fi

    echo -e "${BLUE}Backup Info: $slug${NC}"
    echo ""

    curl -s \
        -H "Authorization: Bearer $HASS_TOKEN" \
        "$HASS_SERVER/api/hassio/backups/$slug/info" | \
        jq '.'
}

# Show help
show_help() {
    echo "Home Assistant Backup and Restore Helper"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create [name]                 Create a new backup"
    echo "  list                          List available backups"
    echo "  info <slug>                   Get backup details"
    echo "  download <slug> [output]      Download a backup"
    echo "  upload <file>                 Upload a backup file"
    echo "  restore <slug> [components]   Restore from backup"
    echo "    components: full (default), homeassistant, addons"
    echo "  help                          Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 create pre-update-backup"
    echo "  $0 list"
    echo "  $0 download abc123 my-backup.tar"
    echo "  $0 restore abc123 homeassistant"
    echo ""
    echo "Environment variables:"
    echo "  HASS_SERVER  Home Assistant URL"
    echo "  HASS_TOKEN   Long-lived access token"
    echo ""
    echo "Note: Some operations require Home Assistant OS or Supervised installation."
}

# Main
main() {
    case "${1:-}" in
        create)
            check_env
            create_backup "$2"
            ;;
        list)
            check_env
            list_backups_supervisor
            ;;
        info)
            check_env
            backup_info "$2"
            ;;
        download)
            check_env
            download_backup "$2" "$3"
            ;;
        upload)
            check_env
            upload_backup "$2"
            ;;
        restore)
            check_env
            restore_backup "$2" "$3"
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
