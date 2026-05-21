# Pantrist Home Assistant Integration

Connect your [Pantrist](https://pantrist.app) account to Home Assistant. Real-time shopping
list, pantry, expiring-soon, and shopping-cart sensors, a native HA **To-Do list** entity
(works with the Lovelace todo card, the Mobile App To-Do tab, and HA Assist voice
commands), plus services for adding, checking, and removing items from automations.

The integration creates **one HA device per Pantrist list** in the account, so multi-list
households get separate sensors / todo entities for each list out of a single OAuth flow.

> The repository name still says "addon" for historical reasons. The current code
> is a Custom Integration (Python, in-process) — the Docker Add-on has been retired.

## Install via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Pantrist-dev&repository=pantrist-ha-addon&category=integration)

1. Install [HACS](https://hacs.xyz/docs/use/download/) if you don't already have it.
2. Open HACS → **Integrations** → ⋮ → **Custom repositories**.
3. Repository URL: `https://github.com/Pantrist-dev/pantrist-ha-addon`
   Category: **Integration** → **Add**.
4. Search for **Pantrist** → **Download** → **Restart Home Assistant**.
5. **Settings → Devices & Services → + Add Integration** → search **Pantrist** → click.
6. Authorize via the browser, pick a list, click **Allow**. Done.

> Pantrist uses PKCE (public client, no secret) and the integration
> ships its own default OAuth implementation — you do **not** need to
> walk through *Application Credentials* before adding the integration.
> If you want to override the client_id with your own (e.g. for a
> self-hosted Pantrist instance), Application Credentials still works
> as a fallback.

## Install manually (no HACS)

```bash
# From your computer, with /config mounted via Samba (or use scp/rsync via SSH)
cp -r custom_components/pantrist /config/custom_components/pantrist
```

Restart Home Assistant, then continue from step 5 above.

## What you get

> Entity IDs below assume a single list named "Home". With multiple lists, HA prefixes
> every entity with the list name (e.g. `sensor.kitchen_shopping_list`,
> `sensor.weekend_pantry`, …). Every entity sits under its own HA device per list.

## Use cases

A few of the automations this integration unlocks once you've connected your Pantrist
account:

- **"Tell me when the shopping list grows past 10 items"** — automation triggers on
  `sensor.<list>_shopping_list` state change, sends a mobile notification listing the
  current items.
- **"Auto-add items I'm running low on"** — when `binary_sensor.<list>_low_stock` turns
  on, walk `state_attr('sensor.<list>_pantry', 'low_stock_items')` and call
  `pantrist.add_to_shopping_list` for each. The bundled blueprint
  (`blueprints/automation/pantrist/low_stock_auto_add.yaml`) does this.
- **"Don't let stuff in the fridge expire"** — daily-at-08:00 trigger reads
  `sensor.<list>_expiring_soon` attributes and pushes a notification listing items
  due within 7 days. Or place `calendar.<list>_pantry_expirations` on a Lovelace
  calendar card for a quiet always-on view.
- **"Add what I just said to the list"** — HA Assist understands `todo.add_item` against
  `todo.<list>_shopping_list` natively, so *"Add milk to the shopping list"* works
  out of the box.
- **"Adjust pantry stock from the dashboard"** — every pantry item is exposed as a
  Number entity (`number.<list>_<item>_amount`); editing the value from a Lovelace
  card sends the delta to Pantrist via `change_pantry_item_amount`.
- **"Show the latest item picture on a wall display"** — bind
  `image.<list>_latest_shopping_item` to a picture-entity card.
- **"NFC-scan the empty jar to restock it"** — stick an NFC tag on items you
  re-buy often. Scan with the HA Companion app (or an ESPHome PN532): the
  bundled `nfc_consume_pantry_item` blueprint decrements the pantry amount via
  `change_pantry_item_amount`. Combined with `low_stock_auto_add`, the item
  appears on your shopping list the moment you scan it past the minimum.

## Data update mechanism

Everything except brand-new list discovery is push-driven. Item add / check / delete
inside a list, list rename, and list deletion all arrive via Socket.IO
(`/lists` namespace) within ~1 s. The integration runs *without* a per-list REST
poll — when the socket reconnects after a disconnect window it triggers a one-shot
`async_request_refresh()` to catch up on anything missed. The single remaining
periodic check is `GET /list` every 15 min to discover lists that have been newly
created or shared into the account, because the Pantrist backend has no
account-scoped socket event for list creation.

If the Socket.IO connection has been down for more than ~5 minutes, the integration
registers a Home Assistant **Repair** issue (Settings → System → Repairs) so users
who depend on real-time updates aren't left guessing. The issue resolves itself
automatically when the connection is restored.

## Known limitations

- **Account scope is fixed at OAuth time.** Switching to a different Pantrist account
  requires deleting the entry and re-adding it. The "Reconfigure" button only
  refreshes tokens for the *same* account.
- **List creation lag.** New lists created in the Pantrist app take up to 15 minutes
  to appear as HA devices. Item changes, rename, and deletion of existing lists are
  real-time. (Closing this gap requires a Pantrist API change — there's no
  account-level socket event today.)
- **Pantry-item write entities are item-scoped.** The Number entities are keyed by
  Pantrist item UUID, so they survive renames but disappear if the underlying item is
  deleted in the Pantrist app. Automations that target them should guard against
  unavailable state.
- **Voice-add is the shopping list only.** HA Assist's `todo.add_item` targets
  `todo.<list>_shopping_list`. Adding to the pantry by voice still requires a
  custom intent (see the `voice_add_to_shopping_list` blueprint).
- **No legacy data import.** This integration starts from the live Pantrist account
  state; it doesn't backfill historical receipts or purchases into HA stats.

### Sensors (per list)

| Entity | Description |
|---|---|
| `sensor.<list>_shopping_list` | Number of items + per-item details |
| `sensor.<list>_pantry` | Pantry item count + low-stock attributes |
| `sensor.<list>_expiring_soon` | Items expiring within a 7-day window |
| `sensor.<list>_shopping_cart` | Items in the intermediate cart |
| `sensor.<list>_next_expiration` | Timestamp sensor — soonest best-before date across the pantry (drives Lovelace countdowns and the calendar card) |

All count sensors carry an `items` attribute with the full per-item payload (uuid,
name, amount, unit, brand, category, image URL, notes). The pantry sensor
additionally exposes `low_stock_count` + `low_stock_items` for items at or below
the configured minimum; the expiring-soon sensor splits its payload into
`expiring_items` and `expired_items` with a `best_before` field per entry.

### Binary sensors (per list)

| Entity | Description |
|---|---|
| `binary_sensor.<list>_low_stock` | ON when any pantry item is at or below its minimum (device class: problem) |
| `binary_sensor.<list>_has_expired_items` | ON when any pantry item is past its earliest best-before (device class: problem) |
| `binary_sensor.<list>_shopping_list_has_items` | ON whenever the shopping list is non-empty — handy for "notify on new item" automations |

### Calendar (per list)

| Entity | Description |
|---|---|
| `calendar.<list>_pantry_expirations` | One all-day calendar event per pantry item with an `earliestBestBefore`. Drops straight into the standard Lovelace calendar card. |

### Todo entity (per list)

| Entity | Description |
|---|---|
| `todo.<list>_shopping_list` | Native HA todo list — works with the Lovelace todo card, the iOS/Android Mobile App "To-Do" tab, and `todo.add_item` / `todo.remove_item` services from automations |

Ticking the box checks the item off Pantrist's shopping list (it's moved to the cart
as you'd expect). Deletes remove it.

### Voice (HA Assist)

The Lovelace voice assistant can read and update the shopping list via the standard
HA todo intents:

| Say | What happens |
|---|---|
| "Add milk to the shopping list" | `pantrist.add_to_shopping_list(name="milk")` |
| "What's on the shopping list?" | HA reads back `todo.<list>_shopping_list` items |
| "Remove eggs from the shopping list" | `todo.remove_item` on the matching item |

The voice add-to-list flow also has a one-click blueprint (see below) that handles
slot extraction explicitly if Assist's built-in todo intent isn't enough for your
language model.

### Services

| Service | Fields | Purpose |
|---|---|---|
| `pantrist.add_to_shopping_list` | `name`, `list_id`* | Add a free-text item |
| `pantrist.add_to_shopping_list_by_barcode` | `barcode`, `list_id`* | Add by EAN/UPC; Pantrist looks up the product |
| `pantrist.check_shopping_list_item` | `item_id`, `list_id`* | Mark item bought (moves it to the cart) |
| `pantrist.delete_shopping_list_item` | `item_id`, `list_id`* | Remove from shopping list |
| `pantrist.add_to_pantry` | `name`, `amount`, `unit_id`, `list_id`* | Add a pantry item by name |
| `pantrist.delete_pantry_item` | `item_id`, `list_id`* | Remove from pantry |
| `pantrist.change_pantry_item_amount` | `item_id`, `change`, `unit_id`, `list_id`* | Increment/decrement pantry amount |

`*` `list_id` is optional — omit it on single-list accounts. With multiple lists,
pass the list UUID (visible in **Settings → Devices & Services → Pantrist → device
identifier**) to target a specific list.

### Diagnostics

**Settings → Devices & Services → Pantrist → ⋮ → Download diagnostics** produces a
JSON dump with the redacted config entry plus per-list status (last successful
refresh, item counts, polling interval). Tokens are redacted automatically — safe
to attach to bug reports.

### Real-time updates

The integration maintains a Socket.IO subscription to Pantrist's `/lists` namespace.
Item additions/changes/deletions made from the mobile app or web UI appear in
Home Assistant within ~1 second. A 5-minute REST poll runs as a safety net.

## Dashboard card (copy-paste)

By default the entity tiles only show the item count. Drop this into your
Lovelace dashboard YAML to see the actual items inline — no extra HACS
plugins required, just core `markdown` + `glance` cards.

```yaml
type: vertical-stack
cards:
  - type: glance
    title: Pantrist
    entities:
      - entity: sensor.pantrist_shopping_list
        name: Shopping
      - entity: sensor.pantrist_pantry
        name: Pantry
      - entity: sensor.pantrist_expiring_soon
        name: Expiring
      - entity: sensor.pantrist_shopping_cart
        name: Cart

  - type: markdown
    content: |
      ## 🛒 Shopping list
      {% set items = state_attr('sensor.pantrist_shopping_list', 'items') or [] %}
      {% if items %}
      {% for item in items %}
      - **{{ item.name }}**{% if item.amount %} · {{ item.amount }}{% if item.unit %} {{ item.unit }}{% endif %}{% endif %}
      {% endfor %}
      {% else %}
      _List is empty._
      {% endif %}

  - type: markdown
    content: |
      ## ⚠️ Expiring soon
      {% set expiring = state_attr('sensor.pantrist_expiring_soon', 'expiring_items') or [] %}
      {% set expired = state_attr('sensor.pantrist_expiring_soon', 'expired_items') or [] %}
      {% if expired %}
      **Already expired:**
      {% for item in expired %}
      - {{ item.name }} (was: {{ item.best_before }})
      {% endfor %}
      {% endif %}
      {% if expiring %}
      **Expiring soon:**
      {% for item in expiring %}
      - {{ item.name }} (by: {{ item.best_before }})
      {% endfor %}
      {% endif %}
      {% if not (expiring or expired) %}
      _Nothing expiring soon. 🎉_
      {% endif %}
```

## Blueprints (one-click automations)

The integration ships three blueprints. Import them via HA:

**Settings → Automations → Blueprints → Import blueprint**

and paste these URLs:

| Blueprint | URL | What it does |
|---|---|---|
| Voice — Add to shopping list | `https://github.com/Pantrist-dev/pantrist-ha-addon/blob/main/blueprints/automation/pantrist/voice_add_to_shopping_list.yaml` | Say "Add milk to the shopping list" (or German "Schreib Milch auf die Einkaufsliste") via HA Assist and the item lands on the list. |
| Low-stock auto-add | `https://github.com/Pantrist-dev/pantrist-ha-addon/blob/main/blueprints/automation/pantrist/low_stock_auto_add.yaml` | Pantry items that fall at or below their configured minimum amount are automatically added to the shopping list. Items already on the list (by name) are skipped, so it composes safely with the server-side `autoRestock` flag — whichever fires first wins. |
| Expiring-soon notification | `https://github.com/Pantrist-dev/pantrist-ha-addon/blob/main/blueprints/automation/pantrist/expiring_notification.yaml` | Fires a notify action (push / TTS / persistent notification — your choice) once per day if any pantry items are within the expiry window. |
| NFC consume pantry item | `https://github.com/Pantrist-dev/pantrist-ha-addon/blob/main/blueprints/automation/pantrist/nfc_consume_pantry_item.yaml` | Scan an NFC tag (Companion app, ESPHome PN532, …) to decrement the bound pantry item. With **Auto-restock when below minimum** enabled (default), one scan does both halves server-side: pantry decrement *and* shopping-list insert, with full article metadata. |

After import: **Automations → + Create from blueprint** → pick one → fill in the inputs → Save.

## Example automations (manual)

```yaml
automation:
  - alias: "Auto-add low stock to shopping list"
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
            - action: pantrist.add_to_shopping_list
              data:
                name: "{{ repeat.item.name }}"
```

## Multiple lists, added live

Every list visible to your Pantrist account becomes its own HA device with its own
set of sensors / binary sensors / calendar / todo entity. List lifecycle is
mostly real-time, with a low-frequency poll covering the one gap:

| Event | Latency | Mechanism |
|---|---|---|
| Item added / checked / deleted inside a list | ~1 s | Socket.IO `data:updated` (push) |
| List renamed | ~1 s | Socket.IO `list:updated` (push) — device name updates live |
| List deleted | ~1 s | Socket.IO `list:deleted` (push) — device + entities removed |
| Socket reconnect after disconnect | ~1 s | Coordinator triggers a one-shot refresh on `connect` to catch up |
| New list created in Pantrist | ≤15 min | `GET /list` reconcile (the only remaining poll) |

The new-list reconcile is needed because the Pantrist backend's socket events
are all room-scoped per list — there's no account-level event you can
subscribe to without already knowing the list id. Once a list is known,
every change to it arrives over the socket.

## Reconfiguration

**Settings → Devices & Services → Pantrist → ⋮ → Reconfigure** lets you re-run
the OAuth flow against the same account without removing the existing entry
(and without losing the automations wired to its entities). Picking a list that
belongs to a different Pantrist account aborts with `wrong_account` — use
*Delete* + *Add Integration* in that case.

## Reauthentication

If you change your Pantrist password or revoke the refresh token, Home Assistant
surfaces a repair notification and asks to reconnect. Click it, run through the
consent flow again, and the existing entry (with all its automations) keeps its
entity IDs — only the tokens are refreshed.

## Remove the integration

1. **Settings → Devices & Services → Pantrist → ⋮ → Delete**. This removes the
   config entry plus every sensor / todo entity it created, and revokes the
   stored OAuth tokens.
2. *(Optional — only if you no longer want Pantrist as an option in the
   "Add Integration" picker)* **HACS → Integrations → Pantrist → ⋮ → Remove**,
   then restart Home Assistant.
3. *(Optional — to clear the OAuth client too)* **Settings → Devices &
   Services → ⋮ → Application Credentials**, find the `pantrist-ha` entry,
   delete.
4. Manual installs: delete `/config/custom_components/pantrist/` and restart HA.

Pantrist data lives in your Pantrist account, not in Home Assistant — removing
the integration only severs the link. The list itself is untouched.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Pantrist" doesn't appear in the Integrations list after install | Restart Home Assistant. `custom_components/` is only scanned at boot. |
| `missing_configuration` in the OAuth dialog | Shouldn't happen with stock install — the integration pre-registers its OAuth client. If it does, you've probably *manually* added an Application Credential row that's overriding the default. Delete that row and reload the integration. |
| `invalid_auth` after OAuth | The token Pantrist returned was rejected by `/list`. Re-run the flow. |
| `cannot_connect` after OAuth | The Pi couldn't reach `api.pantrist.app`. Check network. |
| Browser redirect lands on a Pantrist error page | The Pantrist API needs `my.home-assistant.io` in its redirect-URI whitelist. Confirm the backend deployment is current. |
| Sensors stay `unavailable` after OAuth completes | Check **Settings → System → Logs** for Socket.IO connection errors. Verify the Pi can reach `api.pantrist.app` (try `curl https://api.pantrist.app` from the SSH add-on or shell). |
| `missing_list_id` abort | The Pantrist consent page must include a list picker. Verify the Pantrist web app deployment is current. |
| Entity IDs show as UUID stubs (`pantrist_list_abc12345`) | Pantrist API didn't return a list name during enumeration. Rename the list in the Pantrist app and reload the integration. |

## Development

See [`DEVELOPMENT.md`](DEVELOPMENT.md) for local testing instructions.

## License

MIT. See `LICENSE` (to be added).
