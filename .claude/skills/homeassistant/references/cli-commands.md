# Home Assistant CLI Command Reference

## hass-cli (Remote Access)

Python-based CLI for remote Home Assistant management.

### Installation

```bash
# Fedora/RHEL
sudo dnf install homeassistant-cli

# macOS
brew install homeassistant-cli

# pip (any platform)
pip install homeassistant-cli

# Docker
docker run -it --rm homeassistant/home-assistant-cli
```

### Configuration

Set environment variables for authentication:

```bash
# Required
export HASS_SERVER=http://homeassistant.local:8123
export HASS_TOKEN=<long-lived-access-token>

# Optional
export HASS_INSECURE=true  # Skip SSL verification
```

Obtain token: Home Assistant UI > Profile > Long-Lived Access Tokens > Create Token

### State Commands

```bash
# List all entities
hass-cli state list

# Filter by domain
hass-cli state list --domain light

# Get specific entity
hass-cli state get sensor.temperature

# Get entity with attributes
hass-cli state get sensor.temperature --attributes

# Set entity state (use with caution)
hass-cli state set input_boolean.test_mode on
```

### Service Commands

```bash
# List available services
hass-cli service list

# Call service
hass-cli service call light.turn_on --arguments entity_id=light.living_room

# Call service with multiple arguments
hass-cli service call light.turn_on --arguments \
  entity_id=light.living_room,brightness=128,color_name=blue

# Call service with JSON
hass-cli service call notify.mobile_app --arguments \
  '{"message": "Test notification", "title": "Alert"}'
```

### Event Commands

```bash
# Watch all events
hass-cli event watch

# Watch specific event type
hass-cli event watch state_changed

# Fire custom event
hass-cli event fire custom_event --event-data '{"key": "value"}'
```

### Device and Area Commands

```bash
# List all areas
hass-cli area list

# List all devices
hass-cli device list

# Assign device to area
hass-cli device assign <device_id> <area_id>
```

### Configuration Commands

```bash
# Check configuration validity
hass-cli config check

# Get Home Assistant info
hass-cli info

# Get system health
hass-cli system health
```

### Output Formats

```bash
# JSON output
hass-cli state list --output json

# YAML output
hass-cli state list --output yaml

# Table output (default)
hass-cli state list --output table
```

---

## ha CLI (Supervisor/OS Access)

Go-based CLI for Home Assistant OS and Supervised installations. Access via SSH or Terminal addon.

### Core Commands

```bash
# Check configuration
ha core check

# Get core information
ha core info

# View core logs
ha core logs

# Follow logs in real-time
ha core logs --follow

# Restart Home Assistant
ha core restart

# Stop Home Assistant
ha core stop

# Start Home Assistant
ha core start

# Update Home Assistant
ha core update

# Update to specific version
ha core update --version 2025.1.0

# Rebuild Home Assistant
ha core rebuild

# Get core statistics
ha core stats
```

### Supervisor Commands

```bash
# Get supervisor information
ha supervisor info

# View supervisor logs
ha supervisor logs

# Restart supervisor
ha supervisor restart

# Reload supervisor configuration
ha supervisor reload

# Update supervisor
ha supervisor update

# Repair supervisor issues
ha supervisor repair
```

### Backup Commands

```bash
# List all backups
ha backups list

# Create full backup
ha backups new

# Create named backup
ha backups new --name "pre-update-backup"

# Create partial backup
ha backups new --homeassistant --addons

# Get backup info
ha backups info <slug>

# Restore backup
ha backups restore <slug>

# Restore specific components
ha backups restore <slug> --homeassistant --addons

# Remove backup
ha backups remove <slug>

# Reload backup list
ha backups reload
```

### Add-on Commands

```bash
# List installed addons
ha addons

# Get addon info
ha addons info <slug>

# Start addon
ha addons start <slug>

# Stop addon
ha addons stop <slug>

# Restart addon
ha addons restart <slug>

# Update addon
ha addons update <slug>

# View addon logs
ha addons logs <slug>

# Install addon
ha addons install <slug>

# Uninstall addon
ha addons uninstall <slug>
```

### Host Commands

```bash
# Get host information
ha host info

# Reboot host
ha host reboot

# Shutdown host
ha host shutdown

# Update host
ha host update
```

### Network Commands

```bash
# Get network information
ha network info

# Update network settings
ha network update eth0 --ipv4-method static \
  --ipv4-address 192.168.1.100/24 \
  --ipv4-gateway 192.168.1.1

# Reload network
ha network reload
```

### OS Commands

```bash
# Get OS information
ha os info

# Update OS
ha os update

# Configure boot slot
ha os boot-slot
```

### Hardware Commands

```bash
# Get hardware information
ha hardware info

# Get audio information
ha hardware audio
```

### Resolution Commands

```bash
# Get resolution center info
ha resolution info

# List suggestions
ha resolution suggestion

# Apply suggestion
ha resolution suggestion <uuid>

# Dismiss suggestion
ha resolution dismiss <uuid>
```

### DNS Commands

```bash
# Get DNS information
ha dns info

# Reset DNS
ha dns reset

# Set DNS servers
ha dns options --servers dns://1.1.1.1
```

### Job Commands

```bash
# List running jobs
ha jobs info

# Reset jobs
ha jobs reset
```

### Output Options

```bash
# JSON output
ha core info --raw-json

# No color output
ha core info --no-color

# Specific endpoint
ha core info --api-token <token> --endpoint <url>
```

---

## Common Workflows

### Pre-Update Checklist

```bash
# 1. Create backup
ha backups new --name "pre-$(date +%Y%m%d)-update"

# 2. Check configuration
ha core check

# 3. View current version
ha core info

# 4. Perform update
ha core update

# 5. Monitor logs
ha core logs --follow
```

### Troubleshooting

```bash
# Check system health
ha supervisor info
ha core info

# View recent logs
ha core logs | tail -100
ha supervisor logs | tail -100

# Restart services
ha core restart
ha supervisor restart

# Check for issues
ha resolution info
```

### Remote Monitoring with hass-cli

```bash
# Quick health check
hass-cli info && hass-cli config check

# Monitor specific sensor
watch -n 5 'hass-cli state get sensor.cpu_percent'

# Watch state changes
hass-cli event watch state_changed
```
