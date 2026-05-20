# Pantrist Home Assistant Add-on

[![GitHub Release](https://img.shields.io/github/release/Pantrist-dev/pantrist-ha-addon.svg)](https://github.com/Pantrist-dev/pantrist-ha-addon/releases)

Integrate your [Pantrist](https://pantrist.app) shopping list and pantry with Home Assistant. Real-time updates via Socket.IO — no polling.

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**.
2. Click the overflow menu (⋮) → **Repositories**.
3. Add this URL and click **Add**:
   ```
   https://github.com/Pantrist-dev/pantrist-ha-addon
   ```
4. Find **Pantrist** in the store and click **Install**.
5. Go to the **Configuration** tab and set your options (see below).
6. Click **Save**, then **Start**.

## Connecting your Pantrist account

1. Open the add-on UI in Home Assistant.
2. Click **Connect Pantrist Account**.
3. Log in to Pantrist and pick which list to expose to Home Assistant.
4. After approving, you'll be redirected back — the status page should show **✓ Connected**.

The add-on auto-refreshes its access token every hour using a 30-day refresh token.

## Configuration

| Option                 | Type   | Required | Default                     | Description |
|------------------------|--------|----------|-----------------------------|-------------|
| `socket_url`           | string | yes      | `https://api.pantrist.app`  | Pantrist server base URL (Socket.IO + REST API) |
| `expiry_warning_days`  | int    | yes      | `7`                         | Days ahead to count pantry items as "expiring soon" |
| `custom_ha_url`        | string | no       | `""`                        | Override the OAuth redirect base URL — only needed if your HA is on a custom domain that isn't `homeassistant.local`, `*.ui.nabu.casa`, or a private IP. Example: `https://ha.example.com` |

The add-on reconnects automatically with exponential back-off (2 s → 60 s) on disconnect.

## Entities

| Entity                            | Description |
|-----------------------------------|-------------|
| `sensor.pantrist_shopping_list`   | Number of items on your shopping list |
| `sensor.pantrist_pantry`          | Number of items in your pantry |

### `sensor.pantrist_shopping_list` attributes

| Attribute | Description |
|-----------|-------------|
| `list_id` | Pantrist list ID |
| `items`   | Array of items: `uuid`, `name`, `amount`, `unit`, `brand`, `notes`, `image_url`, `category_uuid` |

### `sensor.pantrist_pantry` attributes

| Attribute         | Description |
|-------------------|-------------|
| `list_id`         | Pantrist list ID |
| `items`           | Array of pantry items |
| `low_stock_count` | Items at or below their configured minimum amount |
| `low_stock_items` | Details of those items |

## Service endpoints

The add-on runs a local HTTP server on port **8099**. Add `rest_command` entries to your `configuration.yaml`:

```yaml
rest_command:
  pantrist_add_to_shopping_list:
    url: "http://localhost:8099/services/add_to_shopping_list"
    method: POST
    content_type: "application/json"
    payload: '{"name": "{{ name }}"}'

  pantrist_check_shopping_list_item:
    url: "http://localhost:8099/services/check_shopping_list_item"
    method: POST
    content_type: "application/json"
    payload: '{"item_id": "{{ item_id }}"}'

  pantrist_delete_shopping_list_item:
    url: "http://localhost:8099/services/delete_shopping_list_item"
    method: POST
    content_type: "application/json"
    payload: '{"list_id": "{{ list_id }}", "item_id": "{{ item_id }}"}'

  pantrist_delete_pantry_item:
    url: "http://localhost:8099/services/delete_pantry_item"
    method: POST
    content_type: "application/json"
    payload: '{"list_id": "{{ list_id }}", "item_id": "{{ item_id }}"}'

  pantrist_change_pantry_amount:
    url: "http://localhost:8099/services/change_pantry_item_amount"
    method: POST
    content_type: "application/json"
    payload: >-
      {"list_id": "{{ list_id }}", "item_id": "{{ item_id }}",
       "change": {{ change }}, "unit_id": "{{ unit_id }}"}

  pantrist_add_to_shopping_list_by_barcode:
    url: "http://localhost:8099/services/add_to_shopping_list_by_barcode"
    method: POST
    content_type: "application/json"
    payload: '{"barcode": "{{ barcode }}"}'

  pantrist_add_to_pantry:
    url: "http://localhost:8099/services/add_to_pantry"
    method: POST
    content_type: "application/json"
    payload: '{"name": "{{ name }}", "amount": {{ amount | default(1) }}, "unit_id": "{{ unit_id | default(\"pieces\") }}"}'
```

## Example automations

### Add item to shopping list via voice

```yaml
automation:
  - alias: "Pantrist – add item via Assist"
    trigger:
      - platform: conversation
        command: "Add {item} to my shopping list"
    action:
      - action: rest_command.pantrist_add_to_shopping_list
        data:
          name: "{{ trigger.slots.item }}"
```

### Auto-add low-stock pantry items to shopping list

```yaml
automation:
  - alias: "Pantrist – auto-add low stock to shopping list"
    trigger:
      - platform: state
        entity_id: sensor.pantrist_pantry
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.pantrist_pantry', 'low_stock_count') | int(0) > 0 }}
    action:
      - repeat:
          for_each: "{{ state_attr('sensor.pantrist_pantry', 'low_stock_items') }}"
          sequence:
            - action: rest_command.pantrist_add_to_shopping_list
              data:
                name: "{{ repeat.item.name }}"
```

### Announce low-stock items on arrival

```yaml
automation:
  - alias: "Pantrist – announce low stock on arrival"
    trigger:
      - platform: zone
        entity_id: person.your_name
        zone: zone.home
        event: enter
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.pantrist_pantry', 'low_stock_count') | int(0) > 0 }}
    action:
      - action: tts.speak
        target:
          entity_id: tts.home_assistant_cloud
        data:
          message: >
            You have {{ state_attr('sensor.pantrist_pantry', 'low_stock_count') }}
            items running low in your pantry.
```

## Dashboard card

```yaml
type: entities
title: Pantrist
entities:
  - entity: sensor.pantrist_shopping_list
    name: Shopping List
    icon: mdi:cart
  - entity: sensor.pantrist_pantry
    name: Pantry
    icon: mdi:fridge
  - type: attribute
    entity: sensor.pantrist_pantry
    attribute: low_stock_count
    name: Low Stock Items
    icon: mdi:alert-circle-outline
```

## Links

- [Pantrist app](https://pantrist.app)
- [Source code](https://github.com/Pantrist-dev/pantrist-ha-addon)
