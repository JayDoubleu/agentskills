# Home Assistant REST API Reference

## Overview

Home Assistant exposes a RESTful API on the same port as the web frontend (default: 8123). The API accepts and returns JSON objects.

## Authentication

All API calls require a Long-Lived Access Token.

### Obtaining a Token

1. Navigate to Home Assistant UI
2. Click on your profile (bottom-left)
3. Scroll to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Name the token and copy the value

### Using the Token

Include in all requests:

```bash
Authorization: Bearer <your-token>
```

Example with curl:

```bash
export HASS_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
export HASS_URL="http://homeassistant.local:8123"

curl -H "Authorization: Bearer $HASS_TOKEN" \
  "$HASS_URL/api/"
```

## API Endpoints

### API Status

```bash
# Check API is running
GET /api/

# Response
{"message": "API running."}
```

### Configuration

```bash
# Get configuration
GET /api/config

# Response includes: location_name, latitude, longitude, elevation,
# unit_system, time_zone, components, version, etc.

# Check configuration validity
POST /api/config/core/check_config

# Response
{"errors": null, "result": "valid"}
```

### States

```bash
# Get all states
GET /api/states

# Get specific entity state
GET /api/states/<entity_id>

# Example
GET /api/states/sensor.temperature

# Response
{
  "entity_id": "sensor.temperature",
  "state": "21.5",
  "attributes": {
    "unit_of_measurement": "°C",
    "friendly_name": "Temperature"
  },
  "last_changed": "2025-01-09T10:30:00+00:00",
  "last_updated": "2025-01-09T10:30:00+00:00"
}

# Set entity state
POST /api/states/<entity_id>
Content-Type: application/json

{
  "state": "25.0",
  "attributes": {
    "unit_of_measurement": "°C"
  }
}
```

### Services

```bash
# Get available services
GET /api/services

# Call a service
POST /api/services/<domain>/<service>
Content-Type: application/json

# Example: Turn on light
POST /api/services/light/turn_on
{
  "entity_id": "light.living_room"
}

# Example: Turn on light with brightness
POST /api/services/light/turn_on
{
  "entity_id": "light.living_room",
  "brightness": 128,
  "color_name": "blue"
}

# Example: Send notification
POST /api/services/notify/mobile_app_phone
{
  "message": "Motion detected",
  "title": "Security Alert"
}

# Response (success)
[
  {
    "entity_id": "light.living_room",
    "state": "on"
  }
]
```

### Events

```bash
# Get event list
GET /api/events

# Fire an event
POST /api/events/<event_type>
Content-Type: application/json

{
  "key": "value"
}

# Response
{"message": "Event custom_event fired."}
```

### History

```bash
# Get state history
GET /api/history/period/<timestamp>

# Example: Last 24 hours for specific entity
GET /api/history/period/2025-01-08T00:00:00Z?filter_entity_id=sensor.temperature

# With end time
GET /api/history/period/2025-01-08T00:00:00Z?end_time=2025-01-09T00:00:00Z
```

### Logbook

```bash
# Get logbook entries
GET /api/logbook/<timestamp>

# Filter by entity
GET /api/logbook/2025-01-08T00:00:00Z?entity=light.living_room
```

### Error Log

```bash
# Get error log
GET /api/error_log
```

### Camera Proxy

```bash
# Get camera snapshot
GET /api/camera_proxy/<camera_entity_id>

# Example
GET /api/camera_proxy/camera.front_door
# Returns JPEG image
```

### Calendars

```bash
# Get calendar list
GET /api/calendars

# Get calendar events
GET /api/calendars/<calendar_entity_id>?start=2025-01-01&end=2025-01-31
```

### Templates

```bash
# Render a template
POST /api/template
Content-Type: application/json

{
  "template": "{{ states('sensor.temperature') }}°C"
}

# Response
"21.5°C"
```

### Intents

```bash
# Handle intent (conversation/voice)
POST /api/intent/handle
Content-Type: application/json

{
  "name": "HassTurnOn",
  "data": {
    "name": "living room lights"
  }
}
```

## Automation Management

### List Automations

```bash
GET /api/config/automation/config

# Returns list of automation configurations
```

### Create/Update Automation

```bash
POST /api/config/automation/config/<automation_id>
Content-Type: application/json

{
  "alias": "Motion Light",
  "description": "Turn on light when motion detected",
  "trigger": [
    {
      "platform": "state",
      "entity_id": "binary_sensor.motion",
      "to": "on"
    }
  ],
  "action": [
    {
      "service": "light.turn_on",
      "target": {
        "entity_id": "light.living_room"
      }
    }
  ]
}
```

### Delete Automation

```bash
DELETE /api/config/automation/config/<automation_id>
```

### Trigger Automation

```bash
POST /api/services/automation/trigger
Content-Type: application/json

{
  "entity_id": "automation.motion_light",
  "skip_condition": true
}
```

## Backup Operations

```bash
# Create backup
POST /api/services/backup/create
Content-Type: application/json

{
  "name": "my_backup"
}
```

## WebSocket API

For real-time communication, use the WebSocket API at:

```
ws://homeassistant.local:8123/api/websocket
```

### Authentication

```json
// Server sends
{"type": "auth_required", "ha_version": "2025.1.0"}

// Client responds
{"type": "auth", "access_token": "<token>"}

// Server confirms
{"type": "auth_ok", "ha_version": "2025.1.0"}
```

### Subscribe to Events

```json
{
  "id": 1,
  "type": "subscribe_events",
  "event_type": "state_changed"
}
```

### Call Service via WebSocket

```json
{
  "id": 2,
  "type": "call_service",
  "domain": "light",
  "service": "turn_on",
  "target": {
    "entity_id": "light.living_room"
  }
}
```

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 405 | Method Not Allowed |

## Example Scripts

### Get All Lights Status

```bash
curl -s -H "Authorization: Bearer $HASS_TOKEN" \
  "$HASS_URL/api/states" | \
  jq '.[] | select(.entity_id | startswith("light.")) | {entity_id, state}'
```

### Toggle Light

```bash
curl -X POST \
  -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}' \
  "$HASS_URL/api/services/light/toggle"
```

### Check If Home Assistant Is Running

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $HASS_TOKEN" \
  "$HASS_URL/api/"
# Returns 200 if running
```

### Get Sensor History

```bash
START=$(date -d "24 hours ago" -Iseconds)
curl -s -H "Authorization: Bearer $HASS_TOKEN" \
  "$HASS_URL/api/history/period/$START?filter_entity_id=sensor.temperature" | \
  jq '.[0][-5:]'  # Last 5 readings
```
