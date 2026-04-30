# Pantrist Home Assistant Addon

Integrates your [Pantrist](https://pantrist.app) shopping list and pantry with Home Assistant using a real-time Socket.IO connection — no polling.

## How it works

The addon connects to the Pantrist Socket.IO server at the `/lists` namespace. Whenever your shopping list or pantry changes, the server emits a `data:updated` event; the addon then re-fetches the affected list via REST and updates the HA sensor state immediately. Mutations (add, check, delete, …) are performed via the REST API, which triggers the Socket.IO event and causes the sensor to update automatically.

## Configuration

| Option       | Type   | Required | Default                        | Description                              |
|--------------|--------|----------|--------------------------------|------------------------------------------|
| `api_token`  | string | yes      | –                              | Firebase ID token from your Pantrist account |
| `socket_url` | string | yes      | `https://api.pantrist.app`     | Pantrist server base URL (used for both Socket.IO and determining the active list) |

The addon reconnects automatically with exponential back-off (2 s → 60 s) on any disconnect.

## Getting your API token

1. Open [app.pantrist.app](https://app.pantrist.app) and sign in.
2. Open browser developer tools → **Application → Local Storage**.
3. Find the key containing `idToken` and copy its value.

Firebase ID tokens expire after **1 hour**. When the token expires the Socket.IO connection will be rejected and the addon logs an authentication error. Update the token in the addon configuration to reconnect.

## Entities created

| Entity ID                        | Description                                   |
|----------------------------------|-----------------------------------------------|
| `sensor.pantrist_shopping_list`  | Number of items on your current shopping list |
| `sensor.pantrist_pantry`         | Number of items in your current pantry        |

### Attributes

**`sensor.pantrist_shopping_list`**
- `list_id` – Pantrist list ID
- `items` – Array of items: `uuid`, `name`, `amount`, `unit`, `brand`, `notes`, `image_url`, `category_uuid`

**`sensor.pantrist_pantry`**
- `list_id` – Pantrist list ID
- `items` – Array of pantry items
- `low_stock_count` – Count of items at or below their configured minimum amount
- `low_stock_items` – Details of those items

## Service endpoints

The addon runs an HTTP server on port **8099**. Add `rest_command` entries to your `configuration.yaml`:

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
```

## Example automations

### Announce low-stock items

```yaml
automation:
  - alias: "Announce low-stock pantry items"
    trigger:
      - platform: state
        entity_id: sensor.pantrist_pantry
    condition:
      - condition: template
        value_template: "{{ state_attr('sensor.pantrist_pantry', 'low_stock_count') | int > 0 }}"
    action:
      - service: tts.speak
        data:
          message: >
            You have {{ state_attr('sensor.pantrist_pantry', 'low_stock_count') }}
            items running low in your pantry.
```

### Add item via voice assistant

```yaml
automation:
  - alias: "Add item to Pantrist shopping list"
    trigger:
      - platform: conversation
        command: "Add {item} to my shopping list"
    action:
      - service: rest_command.pantrist_add_to_shopping_list
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

## Dashboard card example

```yaml
type: entities
title: Pantrist
entities:
  - entity: sensor.pantrist_shopping_list
    name: Shopping List Items
    icon: mdi:cart
  - entity: sensor.pantrist_pantry
    name: Pantry Items
    icon: mdi:fridge
  - type: attribute
    entity: sensor.pantrist_pantry
    attribute: low_stock_count
    name: Low Stock Items
    icon: mdi:alert-circle-outline
```
