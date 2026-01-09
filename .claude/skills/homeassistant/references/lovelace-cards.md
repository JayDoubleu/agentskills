# Lovelace Dashboard Card Reference

## Dashboard Configuration

### Enable YAML Mode

```yaml
# configuration.yaml
lovelace:
  mode: storage  # Keep UI dashboard
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
title: My Home
views:
  - title: Home
    path: home
    icon: mdi:home
    type: sections  # or masonry, panel, sidebar
    sections:
      - type: grid
        cards:
          - type: entities
            entities:
              - sensor.temperature
```

## View Types

### Sections (2025 Recommended)

```yaml
views:
  - title: Living Room
    path: living
    type: sections
    max_columns: 4
    sections:
      - type: grid
        cards:
          - type: tile
            entity: light.living_room
      - type: grid
        title: Climate
        cards:
          - type: thermostat
            entity: climate.living_room
```

### Masonry (Legacy)

```yaml
views:
  - title: Overview
    path: overview
    type: masonry
    cards:
      - type: entities
        entities:
          - light.living_room
```

### Panel (Single Card)

```yaml
views:
  - title: Map
    path: map
    type: panel
    cards:
      - type: map
        entities:
          - person.john
```

## Built-in Cards

### Entity Cards

#### Entities Card

```yaml
- type: entities
  title: Lights
  entities:
    - entity: light.living_room
      name: Living Room
      icon: mdi:ceiling-light
    - entity: light.bedroom
    - type: divider
    - entity: switch.all_lights
      name: All Lights
  show_header_toggle: true
  state_color: true
```

#### Entity Card (Single)

```yaml
- type: entity
  entity: sensor.temperature
  name: Temperature
  icon: mdi:thermometer
  unit: °C
```

#### Tile Card (Modern)

```yaml
- type: tile
  entity: light.living_room
  name: Living Room
  icon: mdi:ceiling-light
  color: amber
  tap_action:
    action: toggle
  features:
    - type: light-brightness
```

### Control Cards

#### Button Card

```yaml
- type: button
  entity: script.movie_mode
  name: Movie Mode
  icon: mdi:movie
  tap_action:
    action: call-service
    service: script.turn_on
    target:
      entity_id: script.movie_mode
  hold_action:
    action: more-info
```

#### Light Card

```yaml
- type: light
  entity: light.living_room
  name: Living Room
```

#### Thermostat Card

```yaml
- type: thermostat
  entity: climate.living_room
  features:
    - type: climate-hvac-modes
      hvac_modes:
        - auto
        - heat
        - cool
        - "off"
```

#### Humidifier Card

```yaml
- type: humidifier
  entity: humidifier.bedroom
```

### Media Cards

#### Media Control Card

```yaml
- type: media-control
  entity: media_player.living_room
```

#### Picture Entity Card

```yaml
- type: picture-entity
  entity: camera.front_door
  camera_view: live
  show_state: false
  show_name: false
```

### Information Cards

#### Sensor Card

```yaml
- type: sensor
  entity: sensor.temperature
  name: Temperature
  graph: line
  hours_to_show: 24
  detail: 2
```

#### History Graph Card

```yaml
- type: history-graph
  title: Temperature History
  entities:
    - sensor.indoor_temperature
    - sensor.outdoor_temperature
  hours_to_show: 24
```

#### Statistics Graph Card

```yaml
- type: statistics-graph
  title: Energy Usage
  entities:
    - sensor.energy_consumption
  stat_types:
    - mean
    - min
    - max
  period:
    calendar:
      period: day
```

#### Logbook Card

```yaml
- type: logbook
  entities:
    - lock.front_door
    - alarm_control_panel.home
  hours_to_show: 24
```

### Layout Cards

#### Grid Card

```yaml
- type: grid
  columns: 3
  square: false
  cards:
    - type: button
      entity: light.living_room
    - type: button
      entity: light.bedroom
    - type: button
      entity: light.kitchen
```

#### Horizontal Stack

```yaml
- type: horizontal-stack
  cards:
    - type: button
      entity: light.living_room
    - type: button
      entity: light.bedroom
```

#### Vertical Stack

```yaml
- type: vertical-stack
  cards:
    - type: entities
      entities:
        - light.living_room
    - type: thermostat
      entity: climate.living_room
```

### Special Cards

#### Conditional Card

```yaml
- type: conditional
  conditions:
    - condition: state
      entity: binary_sensor.motion
      state: "on"
  card:
    type: entities
    entities:
      - binary_sensor.motion
```

#### Markdown Card

```yaml
- type: markdown
  title: Welcome
  content: |
    ## Welcome Home!

    **Temperature:** {{ states('sensor.temperature') }}°C

    **Time:** {{ now().strftime('%H:%M') }}
```

#### Iframe Card

```yaml
- type: iframe
  url: https://grafana.local/dashboard
  aspect_ratio: 16:9
```

#### Map Card

```yaml
- type: map
  entities:
    - entity: person.john
    - entity: zone.home
  default_zoom: 16
  hours_to_show: 24
```

#### Weather Forecast Card

```yaml
- type: weather-forecast
  entity: weather.home
  show_forecast: true
  forecast_type: daily
```

#### Calendar Card

```yaml
- type: calendar
  entities:
    - calendar.family
  initial_view: dayGridMonth
```

#### Shopping List Card

```yaml
- type: shopping-list
```

### Alarm Cards

#### Alarm Panel Card

```yaml
- type: alarm-panel
  entity: alarm_control_panel.home
  states:
    - arm_home
    - arm_away
```

## Custom Cards (HACS)

### Mushroom Cards

Install via HACS for modern UI:

```yaml
# Mushroom Title Card
- type: custom:mushroom-title-card
  title: Living Room
  subtitle: "{{ states('sensor.temperature') }}°C"

# Mushroom Entity Card
- type: custom:mushroom-entity-card
  entity: light.living_room
  icon_color: amber
  tap_action:
    action: toggle

# Mushroom Light Card
- type: custom:mushroom-light-card
  entity: light.living_room
  show_brightness_control: true
  show_color_control: true

# Mushroom Climate Card
- type: custom:mushroom-climate-card
  entity: climate.living_room
  show_temperature_control: true

# Mushroom Chips Card
- type: custom:mushroom-chips-card
  chips:
    - type: entity
      entity: person.john
    - type: entity
      entity: weather.home
    - type: back
```

### Button Card

```yaml
- type: custom:button-card
  entity: light.living_room
  icon: mdi:ceiling-light
  color_type: icon
  tap_action:
    action: toggle
  styles:
    card:
      - border-radius: 12px
    icon:
      - width: 40px
  state:
    - value: "on"
      styles:
        icon:
          - color: amber
```

### Mini Graph Card

```yaml
- type: custom:mini-graph-card
  entities:
    - sensor.temperature
  hours_to_show: 24
  points_per_hour: 4
  line_width: 2
  show:
    labels: true
    points: false
```

### Swipe Card

```yaml
- type: custom:swipe-card
  cards:
    - type: entities
      title: Page 1
      entities:
        - light.living_room
    - type: entities
      title: Page 2
      entities:
        - light.bedroom
```

## Card Actions

### Tap Actions

```yaml
- type: button
  entity: light.living_room
  tap_action:
    action: toggle  # toggle, more-info, call-service, navigate, url, none
```

### Call Service Action

```yaml
tap_action:
  action: call-service
  service: light.turn_on
  target:
    entity_id: light.living_room
  data:
    brightness: 128
```

### Navigate Action

```yaml
tap_action:
  action: navigate
  navigation_path: /lovelace/bedroom
```

### URL Action

```yaml
tap_action:
  action: url
  url_path: https://example.com
```

## Themes and Styling

### Card Mod (HACS)

```yaml
- type: entities
  entities:
    - light.living_room
  card_mod:
    style: |
      ha-card {
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
      }
```

### Theme Selection

```yaml
# View-level theme
views:
  - title: Dark View
    path: dark
    theme: dark_theme
    cards:
      - type: entities
        entities:
          - light.living_room
```

## Complete Dashboard Example

```yaml
title: Home
views:
  - title: Home
    path: home
    icon: mdi:home
    type: sections
    max_columns: 4
    sections:
      # Welcome Section
      - type: grid
        cards:
          - type: markdown
            content: |
              # Welcome Home
              {{ now().strftime('%A, %B %d') }}

      # Quick Controls
      - type: grid
        title: Quick Controls
        cards:
          - type: tile
            entity: light.living_room
            features:
              - type: light-brightness
          - type: tile
            entity: climate.thermostat
          - type: tile
            entity: lock.front_door

      # Climate
      - type: grid
        title: Climate
        cards:
          - type: thermostat
            entity: climate.living_room
          - type: sensor
            entity: sensor.temperature
            graph: line
            hours_to_show: 24

      # Security
      - type: grid
        title: Security
        cards:
          - type: alarm-panel
            entity: alarm_control_panel.home
          - type: picture-entity
            entity: camera.front_door
            camera_view: live

      # Media
      - type: grid
        title: Media
        cards:
          - type: media-control
            entity: media_player.living_room

  - title: Lights
    path: lights
    icon: mdi:lightbulb-group
    type: sections
    sections:
      - type: grid
        title: Living Room
        cards:
          - type: tile
            entity: light.living_room_ceiling
          - type: tile
            entity: light.living_room_lamp
      - type: grid
        title: Bedroom
        cards:
          - type: tile
            entity: light.bedroom_ceiling
          - type: tile
            entity: light.bedroom_nightstand
```

## Tips and Best Practices

1. **Use Sections view** for modern, responsive layouts
2. **Tile cards** are recommended over button cards for entities
3. **Install Mushroom cards** via HACS for consistent modern UI
4. **Use conditional cards** to show/hide based on state
5. **Group related entities** in sections with titles
6. **Test on mobile** - use responsive columns
7. **Use themes** for consistent styling
8. **Refresh dashboard** after YAML changes (no restart needed)
