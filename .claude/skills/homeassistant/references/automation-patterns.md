# Home Assistant Automation Patterns

## Automation Structure

Every automation requires these components:

```yaml
automation:
  - id: "unique_automation_id"  # Required for traces
    alias: "Human Readable Name"
    description: "What this automation does"
    mode: single  # single, restart, queued, parallel
    trace:
      stored_traces: 10  # Optional: default is 5
    triggers:
      - trigger: <trigger_type>
    conditions:  # Optional
      - condition: <condition_type>
    actions:
      - action: <action>
```

## Common Trigger Patterns

### State Change

```yaml
triggers:
  # Simple state change
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"

  # From specific state
  - trigger: state
    entity_id: binary_sensor.motion
    from: "off"
    to: "on"

  # Any change (omit to/from)
  - trigger: state
    entity_id: sensor.temperature

  # Attribute change
  - trigger: state
    entity_id: climate.thermostat
    attribute: temperature

  # Duration (state held for time)
  - trigger: state
    entity_id: binary_sensor.motion
    to: "off"
    for:
      minutes: 5
```

### Time-Based

```yaml
triggers:
  # Specific time
  - trigger: time
    at: "07:30:00"

  # Multiple times
  - trigger: time
    at:
      - "07:30:00"
      - "19:00:00"

  # Time pattern (every 5 minutes)
  - trigger: time_pattern
    minutes: "/5"

  # Sunrise/Sunset
  - trigger: sun
    event: sunrise
    offset: "-00:30:00"  # 30 min before

  # Sunset
  - trigger: sun
    event: sunset
    offset: "00:15:00"  # 15 min after
```

### Numeric State

```yaml
triggers:
  # Above threshold
  - trigger: numeric_state
    entity_id: sensor.temperature
    above: 25

  # Below threshold
  - trigger: numeric_state
    entity_id: sensor.humidity
    below: 30

  # Range
  - trigger: numeric_state
    entity_id: sensor.temperature
    above: 20
    below: 25

  # With duration
  - trigger: numeric_state
    entity_id: sensor.temperature
    above: 30
    for:
      minutes: 10
```

### Event-Based

```yaml
triggers:
  # Custom event
  - trigger: event
    event_type: custom_event
    event_data:
      key: value

  # Mobile app notification action
  - trigger: event
    event_type: mobile_app_notification_action
    event_data:
      action: "TURN_OFF_LIGHTS"

  # Device trigger (Zigbee button)
  - trigger: device
    domain: zha
    device_id: <device_id>
    type: remote_button_short_press
    subtype: button_1
```

### Template Trigger

```yaml
triggers:
  - trigger: template
    value_template: >
      {{ states('sensor.temperature') | float > 25 and
         is_state('binary_sensor.window', 'off') }}
```

## Condition Patterns

### State Conditions

```yaml
conditions:
  # Simple state check
  - condition: state
    entity_id: binary_sensor.home
    state: "on"

  # Multiple states (OR)
  - condition: state
    entity_id: alarm_control_panel.home
    state:
      - "armed_home"
      - "armed_away"

  # Attribute check
  - condition: state
    entity_id: climate.thermostat
    attribute: hvac_action
    state: "heating"
```

### Time Conditions

```yaml
conditions:
  # Time range
  - condition: time
    after: "07:00:00"
    before: "23:00:00"

  # Weekdays only
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri

  # Weekend
  - condition: time
    weekday:
      - sat
      - sun
```

### Numeric Conditions

```yaml
conditions:
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 20
    below: 25
```

### Template Conditions

```yaml
conditions:
  - condition: template
    value_template: >
      {{ now().hour >= 22 or now().hour < 6 }}
```

### Logical Conditions

```yaml
conditions:
  # AND (default)
  - condition: and
    conditions:
      - condition: state
        entity_id: binary_sensor.home
        state: "on"
      - condition: time
        after: "18:00:00"

  # OR
  - condition: or
    conditions:
      - condition: state
        entity_id: person.john
        state: "home"
      - condition: state
        entity_id: person.jane
        state: "home"

  # NOT
  - condition: not
    conditions:
      - condition: state
        entity_id: alarm_control_panel.home
        state: "disarmed"
```

## Action Patterns

### Service Calls

```yaml
actions:
  # Simple service call
  - action: light.turn_on
    target:
      entity_id: light.living_room

  # With data
  - action: light.turn_on
    target:
      entity_id: light.living_room
    data:
      brightness: 128
      transition: 2

  # Multiple targets
  - action: light.turn_off
    target:
      entity_id:
        - light.living_room
        - light.bedroom
      area_id: kitchen
```

### Delays and Waits

```yaml
actions:
  - action: light.turn_on
    target:
      entity_id: light.porch

  - delay:
      minutes: 5

  - action: light.turn_off
    target:
      entity_id: light.porch
```

### Wait for Trigger

```yaml
actions:
  - action: light.turn_on
    target:
      entity_id: light.hallway

  - wait_for_trigger:
      - trigger: state
        entity_id: binary_sensor.motion_hallway
        to: "off"
        for:
          minutes: 2
    timeout:
      minutes: 10
    continue_on_timeout: true

  - action: light.turn_off
    target:
      entity_id: light.hallway
```

### Choose (If/Else)

```yaml
actions:
  - choose:
      - conditions:
          - condition: state
            entity_id: input_select.mode
            state: "Movie"
        sequence:
          - action: light.turn_on
            target:
              entity_id: light.living_room
            data:
              brightness: 30
      - conditions:
          - condition: state
            entity_id: input_select.mode
            state: "Reading"
        sequence:
          - action: light.turn_on
            target:
              entity_id: light.living_room
            data:
              brightness: 255
    default:
      - action: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness: 180
```

### Repeat

```yaml
actions:
  # Count-based
  - repeat:
      count: 3
      sequence:
        - action: light.toggle
          target:
            entity_id: light.alert
        - delay:
            seconds: 1

  # While condition
  - repeat:
      while:
        - condition: state
          entity_id: binary_sensor.motion
          state: "on"
      sequence:
        - action: light.turn_on
          target:
            entity_id: light.hallway
        - delay:
            minutes: 1

  # Until condition
  - repeat:
      until:
        - condition: state
          entity_id: sensor.temperature
          state: "22"
      sequence:
        - action: climate.set_temperature
          target:
            entity_id: climate.thermostat
          data:
            temperature: 22
        - delay:
            minutes: 5
```

### Variables

```yaml
actions:
  - variables:
      brightness_level: >
        {% if now().hour < 8 or now().hour > 20 %}
          100
        {% else %}
          255
        {% endif %}

  - action: light.turn_on
    target:
      entity_id: light.living_room
    data:
      brightness: "{{ brightness_level }}"
```

### Parallel Actions

```yaml
actions:
  - parallel:
      - action: light.turn_on
        target:
          entity_id: light.living_room
      - action: media_player.play_media
        target:
          entity_id: media_player.speaker
        data:
          media_content_id: doorbell.mp3
          media_content_type: music
```

## Debugging Patterns

### Enable Traces

Always include `id` for trace support:

```yaml
automation:
  - id: "motion_lights_001"
    alias: "Motion Lights"
    trace:
      stored_traces: 15  # Keep more traces for debugging
```

### Debug Notifications

```yaml
actions:
  - action: notify.mobile_app
    data:
      message: >
        Automation triggered.
        Trigger: {{ trigger.to_state.state }}
        Time: {{ now().strftime('%H:%M:%S') }}
```

### Debug Variables

```yaml
actions:
  - variables:
      debug_info: >
        Trigger entity: {{ trigger.entity_id }}
        From: {{ trigger.from_state.state }}
        To: {{ trigger.to_state.state }}

  - action: persistent_notification.create
    data:
      title: "Automation Debug"
      message: "{{ debug_info }}"
```

## Complete Examples

### Motion-Activated Lights with Timeout

```yaml
automation:
  - id: "motion_lights_living_room"
    alias: "Motion Lights - Living Room"
    description: "Turn on lights when motion detected, off after 5 min no motion"
    mode: restart
    trace:
      stored_traces: 10
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion_living_room
        to: "on"
    conditions:
      - condition: numeric_state
        entity_id: sensor.living_room_illuminance
        below: 50
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness_pct: >
            {% if now().hour >= 22 or now().hour < 6 %}
              30
            {% else %}
              100
            {% endif %}
      - wait_for_trigger:
          - trigger: state
            entity_id: binary_sensor.motion_living_room
            to: "off"
            for:
              minutes: 5
        timeout:
          minutes: 30
      - action: light.turn_off
        target:
          entity_id: light.living_room
        data:
          transition: 5
```

### Presence-Based Thermostat

```yaml
automation:
  - id: "thermostat_away_mode"
    alias: "Thermostat Away Mode"
    description: "Adjust temperature when everyone leaves"
    mode: single
    trace:
      stored_traces: 10
    triggers:
      - trigger: state
        entity_id: group.family
        to: "not_home"
        for:
          minutes: 10
    conditions:
      - condition: state
        entity_id: input_boolean.vacation_mode
        state: "off"
    actions:
      - action: climate.set_temperature
        target:
          entity_id: climate.thermostat
        data:
          temperature: 18
      - action: notify.mobile_app
        data:
          message: "Everyone left. Thermostat set to away mode (18°C)"
```

### Notification with Actionable Buttons

```yaml
automation:
  - id: "doorbell_notification"
    alias: "Doorbell Notification"
    triggers:
      - trigger: state
        entity_id: binary_sensor.doorbell
        to: "on"
    actions:
      - action: notify.mobile_app
        data:
          title: "Doorbell"
          message: "Someone is at the door"
          data:
            actions:
              - action: "UNLOCK_DOOR"
                title: "Unlock Door"
              - action: "IGNORE"
                title: "Ignore"
            image: /api/camera_proxy/camera.front_door

  - id: "doorbell_action_unlock"
    alias: "Doorbell Action - Unlock"
    triggers:
      - trigger: event
        event_type: mobile_app_notification_action
        event_data:
          action: "UNLOCK_DOOR"
    actions:
      - action: lock.unlock
        target:
          entity_id: lock.front_door
```
