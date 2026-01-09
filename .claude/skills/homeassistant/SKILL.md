---
name: Home Assistant
description: This skill should be used when the user asks to "deploy Home Assistant", "configure Home Assistant", "update Home Assistant", "manage HA automations", "create Lovelace dashboard", "connect to Home Assistant CLI", "verify automation", "debug automation", "backup Home Assistant", "restore HA backup", "test automation trace", "create dashboard card", "hass-cli setup", "ha core restart", or mentions Home Assistant, hass-cli, ha CLI commands, Lovelace YAML, or HA deployment workflows.
---

# Home Assistant Skill

Manage Home Assistant instances including deployment operations, remote CLI access, automation verification, and Lovelace dashboard development.

## Quick Start

```bash
# Check configuration before restart
ha core check

# Restart Home Assistant
ha core restart

# Create backup
ha backups new --name "backup-$(date +%Y%m%d)"

# View logs
ha core logs --follow
```

## CLI Access Methods

Home Assistant provides two distinct CLI tools for different use cases.

### hass-cli (Remote Access)

Use `hass-cli` for remote management from any machine. Requires configuration:

```bash
export HASS_SERVER=http://homeassistant.local:8123
export HASS_TOKEN=<long-lived-access-token>
```

**Installation options:**
- Fedora/RHEL: `dnf install homeassistant-cli`
- macOS: `brew install homeassistant-cli`
- pip: `pip install homeassistant-cli`

**Common operations:**
- `hass-cli state list` - List all entity states
- `hass-cli state get sensor.temperature` - Get specific entity
- `hass-cli service call light.turn_on --arguments entity_id=light.living_room`
- `hass-cli event watch` - Subscribe to all events
- `hass-cli area list` / `hass-cli device list` - Inventory

### ha CLI (Supervisor Access)

Use the `ha` command directly on Home Assistant OS via SSH addon or Terminal addon.

**Core operations:**
- `ha core check` - Validate configuration
- `ha core info` - System information
- `ha core logs` - View core logs
- `ha core restart` - Restart Home Assistant
- `ha core update` - Update to latest version

**Supervisor operations:**
- `ha supervisor info` - Supervisor details
- `ha supervisor logs` - Supervisor logs
- `ha supervisor restart` - Restart supervisor

See `references/cli-commands.md` for complete command reference.

## Deployment Workflows

### Creating Backups

**Via CLI (on device):**
```bash
ha backups new --name "pre-update-backup"
ha backups list
```

**Via REST API (remote):**
```bash
curl -X POST -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json" \
  http://homeassistant.local:8123/api/services/backup/create
```

**Best practice:** Store backups off-device (NAS, cloud storage, HA Cloud).

### Restoring Backups

```bash
# List available backups
ha backups list

# Restore specific backup
ha backups restore <slug> --homeassistant --addons

# For large backups, upload via SCP first
scp backup.tar root@homeassistant.local:/backup/
```

**Post-restore:** If addons show as not running after restore, execute `ha supervisor restart`.

### Updating Home Assistant

```bash
# Check current version
ha core info

# Update to latest
ha core update

# Or update to specific version
ha core update --version 2025.1.0
```

## Automation Verification

### YAML Validation

Before restarting, validate configuration:

1. **UI Method:** Developer Tools > YAML > Check Configuration (requires Advanced Mode)
2. **CLI Method:** `ha core check`
3. **REST API:**
   ```bash
   curl -X POST -H "Authorization: Bearer $HASS_TOKEN" \
     http://homeassistant.local:8123/api/config/core/check_config
   ```

### Automation Traces

Enable trace storage for debugging by adding `id` and `trace` to automations:

```yaml
automation:
  - id: "motion_lights_living_room"
    alias: "Motion Lights - Living Room"
    trace:
      stored_traces: 10
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion_living_room
        to: "on"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
```

**Accessing traces:**
- UI: Settings > Automations > Select automation > Traces tab
- Traces show execution path, condition evaluations, and action results

### Testing Automations

**Manual trigger:**
1. Developer Tools > Actions
2. Select "Automation: Trigger"
3. Choose automation entity
4. Toggle "Skip conditions" if needed
5. Execute and observe trace

**Template debugging:**
Test Jinja2 templates in Developer Tools > Templates before using in automations.

See `references/automation-patterns.md` for common patterns and debugging techniques.

## Lovelace Dashboard Development

### YAML Mode Setup

Enable YAML dashboards alongside UI-managed default:

```yaml
# configuration.yaml
lovelace:
  mode: storage
  dashboards:
    custom-yaml:
      mode: yaml
      title: Custom Dashboard
      icon: mdi:view-dashboard
      show_in_sidebar: true
      filename: dashboards/custom.yaml
```

### Dashboard Structure

```yaml
# dashboards/custom.yaml
title: My Dashboard
views:
  - title: Home
    path: home
    icon: mdi:home
    sections:
      - type: grid
        cards:
          - type: entities
            entities:
              - sensor.temperature
              - sensor.humidity
          - type: button
            entity: light.living_room
            tap_action:
              action: toggle
```

### Modern Card Options (2025)

- **Mushroom Cards:** Modern, attractive design (install via HACS)
- **Sections Layout:** Drag-and-drop organization
- **Custom Button Card:** Highly customizable buttons
- **Swipe Card:** Mobile-friendly card navigation

**Live reload:** Changes to YAML dashboards apply immediately - use refresh button in dashboard menu (no restart required).

See `references/lovelace-cards.md` for card reference and examples.

## REST API Quick Reference

**Authentication:**
```bash
export HASS_TOKEN="<long-lived-access-token>"
```

**Common endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API status check |
| `/api/states` | GET | All entity states |
| `/api/states/<entity_id>` | GET | Single entity state |
| `/api/services/<domain>/<service>` | POST | Call service |
| `/api/config/core/check_config` | POST | Validate config |

**Success indicators:** Status codes 200 or 201.

See `references/rest-api.md` for complete endpoint documentation.

## Workflow Scripts

Utility scripts are available in `scripts/`:

- **`validate-config.sh`** - Validate configuration before restart
- **`test-automation.sh`** - Trigger and trace automation
- **`backup-restore.sh`** - Backup/restore helper with verification

## Additional Resources

### Reference Files

Detailed documentation in `references/`:
- **`cli-commands.md`** - Complete CLI command reference
- **`rest-api.md`** - REST API endpoints and examples
- **`automation-patterns.md`** - Common automation patterns
- **`lovelace-cards.md`** - Dashboard card reference

### Example Files

Working examples in `examples/`:
- **`hass-cli-setup.sh`** - CLI environment setup
- **`automation-example.yaml`** - Sample automation with traces
- **`dashboard-example.yaml`** - Complete Lovelace dashboard

### External Documentation

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [hass-cli Repository](https://github.com/home-assistant-ecosystem/home-assistant-cli)
- [ha CLI Repository](https://github.com/home-assistant/cli)
- [Automation Documentation](https://www.home-assistant.io/docs/automation/)
- [Dashboard Documentation](https://www.home-assistant.io/dashboards/)
