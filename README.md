# Pantrist Home Assistant Integration

Connect your [Pantrist](https://pantrist.app) account to Home Assistant. Real-time shopping
list, pantry, expiring-soon, and shopping-cart sensors, plus services for adding,
checking, and removing items from automations.

> The repository name still says "addon" for historical reasons. The current code
> is a Custom Integration (Python, in-process) — the Docker Add-on has been retired.

## Install via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Pantrist-dev&repository=pantrist-ha-addon&category=integration)

1. Install [HACS](https://hacs.xyz/docs/use/download/) if you don't already have it.
2. Open HACS → **Integrations** → ⋮ → **Custom repositories**.
3. Repository URL: `https://github.com/Pantrist-dev/pantrist-ha-addon`
   Category: **Integration** → **Add**.
4. Search for **Pantrist** → **Download** → **Restart Home Assistant**.
5. **Settings → Devices & Services → ⋮ → Application Credentials → Add Credential**:
   - Integration: **Pantrist**
   - Client ID: `pantrist-ha`
   - Client Secret: *(leave blank — we use PKCE)*
6. **Settings → Devices & Services → + Add Integration** → search **Pantrist** → click.
7. Authorize via the browser, pick a list, click **Allow**. Done.

## Install manually (no HACS)

```bash
# From your computer, with /config mounted via Samba (or use scp/rsync via SSH)
cp -r custom_components/pantrist /config/custom_components/pantrist
```

Restart Home Assistant, then continue from step 5 above.

## What you get

### Sensors

| Entity | Description |
|---|---|
| `sensor.pantrist_shopping_list` | Number of items + per-item details |
| `sensor.pantrist_pantry` | Pantry item count + low-stock attributes |
| `sensor.pantrist_expiring_soon` | Items expiring within a 7-day window |
| `sensor.pantrist_shopping_cart` | Items in the intermediate cart |

All sensors carry an `items` attribute with the full per-item payload (uuid, name,
amount, unit, brand, category, image URL, notes).

### Services

| Service | Fields | Purpose |
|---|---|---|
| `pantrist.add_to_shopping_list` | `name` | Add a free-text item |
| `pantrist.check_shopping_list_item` | `item_id` | Mark item bought |
| `pantrist.delete_shopping_list_item` | `item_id` | Remove from shopping list |
| `pantrist.delete_pantry_item` | `item_id` | Remove from pantry |
| `pantrist.change_pantry_item_amount` | `item_id`, `change`, `unit_id` | Increment/decrement pantry amount |

### Real-time updates

The integration maintains a Socket.IO subscription to Pantrist's `/lists` namespace.
Item additions/changes/deletions made from the mobile app or web UI appear in
Home Assistant within ~1 second — no polling.

## Example automations

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

## Troubleshooting

| Problem | Fix |
|---|---|
| "Pantrist" doesn't appear in the Integrations list after install | Restart Home Assistant. `custom_components/` is only scanned at boot. |
| `missing_configuration` in the OAuth dialog | Add the Application Credential first (see step 5 above). |
| Browser redirect lands on a Pantrist error page | The Pantrist API needs `my.home-assistant.io` in its redirect-URI whitelist. Confirm the backend deployment is current. |
| Sensors stay `unavailable` after OAuth completes | Check **Settings → System → Logs** for Socket.IO connection errors. Verify the Pi can reach `api.pantrist.app` (try `curl https://api.pantrist.app` from the SSH add-on or shell). |
| `missing_list_id` abort | The Pantrist consent page must include a list picker. Verify the Pantrist web app deployment is current. |

## Development

See [`DEVELOPMENT.md`](DEVELOPMENT.md) for local testing instructions.

## License

MIT. See `LICENSE` (to be added).
