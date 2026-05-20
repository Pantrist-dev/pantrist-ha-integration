---
title: Pantrist
description: Instructions on how to integrate your Pantrist shopping list and pantry with Home Assistant.
ha_category:
  - Shopping List
ha_iot_class: Cloud Push
ha_release: "2025.1"
ha_codeowners:
  - "@nlueg"
ha_domain: pantrist
ha_platforms:
  - sensor
ha_integration_type: hub
---

[Pantrist](https://pantrist.app) is a grocery and household management app that lets
you maintain a shared shopping list and a digital pantry inventory across iOS, Android,
and web. It supports multi-user lists, barcode scanning, best-before tracking, and
home screen widgets.

The **Pantrist** addon for Home Assistant connects to the Pantrist backend over a
persistent Socket.IO connection. Sensor states are updated in real time whenever your
shopping list or pantry changes in the app — no polling required.

## Prerequisites

- A running [Pantrist](https://pantrist.app) account.
- The **Pantrist** Home Assistant addon installed and running.
- A Firebase ID token for your Pantrist account (see [Getting your API token](#getting-your-api-token)).

## Getting your API token

The addon authenticates using a Firebase ID token from your Pantrist session.

1. Open the Pantrist web app at [app.pantrist.app](https://app.pantrist.app) and sign in.
2. Open your browser's developer tools and go to **Application → Local Storage**.
3. Find the key that contains `idToken` — copy its value.

{% note %}
Firebase ID tokens expire after **1 hour**. When the token expires, the WebSocket
connection will be rejected and the addon will log an authentication error. Re-enter
a fresh token in the addon configuration to reconnect.
{% endnote %}

## Configuration

Install and configure the addon from the Home Assistant add-on store:

1. Navigate to **Settings → Add-ons → Add-on Store**.
2. Click the overflow menu (⋮) and select **Repositories**.
3. Add the Pantrist repository URL and click **Add**.
4. Find the **Pantrist** addon and click **Install**.
5. Go to the addon's **Configuration** tab and set your options.

| Option                | Default                        | Description |
|-----------------------|-------------------------------|-------------|
| `refresh_token`       | _(recommended)_               | OAuth refresh token — auto-renews the access token every hour |
| `api_token`           | _(fallback)_                  | Static Firebase ID token (expires after 1 hour; use `refresh_token` instead) |
| `socket_url`          | `https://api.pantrist.app`    | Pantrist server base URL (Socket.IO + REST API) |
| `expiry_warning_days` | `7`                           | Items expiring within this many days appear in `sensor.pantrist_expiring_soon` |

At least one of `refresh_token` or `api_token` is required. `refresh_token` is strongly preferred — when present, the addon renews its access token automatically without any user action.

6. Click **Save** and then **Start** the addon.

The addon also exposes a local HTTP service on port **8099** which you can use with
[`rest_command`](#actions) to call Pantrist actions from automations.

## Entities

### Sensors

#### Shopping Cart (`sensor.pantrist_shopping_cart`)

Tracks items in your Pantrist shopping cart (the intermediate list you fill while shopping before checking out).

| Attribute | Description |
|-----------|-------------|
| `list_id` | Internal Pantrist list ID |
| `items`   | Array of cart items (same fields as shopping list items) |

#### Expiring Soon (`sensor.pantrist_expiring_soon`)

Tracks pantry items that are approaching or past their best-before date.

| Attribute        | Description |
|------------------|-------------|
| `warning_days`   | The configured lookahead window |
| `expiring_count` | Items expiring within `warning_days` |
| `expiring_items` | Array of those items (same fields as pantry items, plus `best_before`) |
| `expired_count`  | Items already past their best-before date |
| `expired_items`  | Array of those items |

The sensor state (numeric) equals `expiring_count + expired_count`, making it easy to use as a badge or condition trigger.

{% tip %}
Use this sensor in an automation to get a daily briefing of what to use up first,
or to automatically add expired items to your shopping list.
{% endtip %}

#### Shopping List (`sensor.pantrist_shopping_list`)

Tracks the number of items on your current Pantrist shopping list.

| Attribute   | Description |
|-------------|-------------|
| `list_id`   | Internal Pantrist list ID |
| `items`     | Array of all items currently on the list |

Each entry in `items` contains:

| Field         | Description |
|---------------|-------------|
| `uuid`        | Unique item ID |
| `name`        | Item name |
| `amount`      | Quantity |
| `unit`        | Unit of measurement (e.g. `pieces`, `g`, `l`) |
| `brand`       | Brand name (if set) |
| `notes`       | Free-text notes (if set) |
| `image_url`   | Product image (if available) |
| `category_uuid` | Category reference |

#### Pantry (`sensor.pantrist_pantry`)

Tracks the total number of items stored in your current Pantrist pantry.

| Attribute         | Description |
|-------------------|-------------|
| `list_id`         | Internal Pantrist list ID |
| `items`           | Array of all pantry items |
| `low_stock_count` | Number of items whose current amount is at or below their configured minimum |
| `low_stock_items` | Array of low-stock items (same fields as `items`) |

{% tip %}
Use `low_stock_count` as an automation trigger to get notified when you are running
low on items, or to automatically add them to your shopping list.
{% endtip %}

## Actions

The addon exposes a local HTTP API on port **8099** that Home Assistant can call via
[`rest_command`](https://www.home-assistant.io/integrations/rest_command/). Add the
following to your `configuration.yaml`:

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

### Action reference

#### `rest_command.pantrist_add_to_shopping_list`

Adds an item to your current shopping list by name. Pantrist matches the name against
your article catalog and assigns the correct category automatically.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `name`    | string | Name of the item to add |

#### `rest_command.pantrist_check_shopping_list_item`

Marks an item as bought. Depending on your list settings, the item is either removed,
moved to the pantry, or placed in the shopping cart.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `item_id` | string | `uuid` of the item (from the `items` attribute) |

#### `rest_command.pantrist_delete_shopping_list_item`

Permanently removes an item from the shopping list without adding it to the pantry.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `list_id` | string | `list_id` attribute of `sensor.pantrist_shopping_list` |
| `item_id` | string | `uuid` of the item |

#### `rest_command.pantrist_delete_pantry_item`

Removes an item from the pantry.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `list_id` | string | `list_id` attribute of `sensor.pantrist_pantry` |
| `item_id` | string | `uuid` of the item |

#### `rest_command.pantrist_add_to_pantry`

Adds an item directly to your pantry by name (bypasses the shopping list).

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `name`    | string | yes      | Item name (can include quantity, e.g. `"2 kg potatoes"`) |
| `amount`  | number | no       | Quantity (default `1`) |
| `unit_id` | string | no       | Unit (default `"pieces"`) |

#### `rest_command.pantrist_add_to_shopping_list_by_barcode`

Looks up a barcode in the Pantrist product database and adds the matching article to your shopping list.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `barcode` | string | EAN/UPC barcode number |

Returns a 404 error if the barcode is not in the Pantrist database.

#### `rest_command.pantrist_change_pantry_amount`

Adjusts the stored amount of a pantry item by a positive or negative delta.

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `list_id` | string | `list_id` attribute of `sensor.pantrist_pantry` |
| `item_id` | string | `uuid` of the item |
| `change`  | number | Amount to add (positive) or subtract (negative) |
| `unit_id` | string | Unit matching the item's unit (e.g. `pieces`, `g`, `ml`) |

## Automation examples

### Announce low-stock items when arriving home

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
            Heads up — you have
            {{ state_attr('sensor.pantrist_pantry', 'low_stock_count') }}
            items running low in your pantry.
```

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

### Automatically add low-stock pantry items to shopping list

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

### Notify household members when the shopping list grows

```yaml
automation:
  - alias: "Pantrist – notify when shopping list changes"
    trigger:
      - platform: state
        entity_id: sensor.pantrist_shopping_list
    condition:
      - condition: template
        value_template: >
          {{ trigger.to_state.state | int(0) > trigger.from_state.state | int(0) }}
    action:
      - action: notify.mobile_app_your_phone
        data:
          title: "Shopping list updated"
          message: >
            {{ trigger.to_state.state }} item(s) on the shopping list.
```

## Dashboard card

To display your Pantrist data on a dashboard:

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

## Known limitations

- **Token expiry (static token only)** — If you configure `api_token` instead of
  `refresh_token`, it expires after 1 hour and must be replaced manually. Use
  `refresh_token` to avoid this entirely.
- **List switching** — The addon polls every 5 minutes to detect when you switch your
  active list in the app. Real-time list switching is not instant but resolves within 5 minutes.
