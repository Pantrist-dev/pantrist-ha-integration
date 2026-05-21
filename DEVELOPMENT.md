# Pantrist Integration — Development

Local development of the Pantrist Custom Integration against a running Home
Assistant instance (typically a Raspberry Pi with HAOS, or a UTM VM on Mac).

## Prerequisites

- A Home Assistant instance reachable at `http://homeassistant.local:8123` (or your custom hostname).
- The **Samba share** add-on installed in HA, with a password set — used to mount `/config/` on your Mac.
- Pantrist API + App deployments containing the OAuth flow changes (`pantrist-ha` client, `my.home-assistant.io` redirect-URI whitelist, `/oauth/authorize` page).

## One-time setup

### Register the OAuth client in HA

Before adding the integration, register the Application Credential. Without
this, the OAuth dialog aborts with `missing_configuration`.

1. In HA: **Settings → Devices & Services → ⋮ → Application Credentials → Add Credential**.
2. Fill in:
   - Integration: **Pantrist**
   - Client ID: `pantrist-ha`
   - Client Secret: *(leave empty — PKCE only)*
   - Name: Pantrist (or anything)
3. **Add**.

## Install the integration files

### Via Samba (recommended for iteration)

```bash
# 1. Mount the HA config share (Finder: Cmd+K → smb://homeassistant.local → log in → mount `config`)
open "smb://homeassistant.local"

# 2. Copy the integration
mkdir -p /Volumes/config/custom_components
cp -r custom_components/pantrist /Volumes/config/custom_components/pantrist

# 3. Restart HA: Settings → System → Restart
```

### Via SSH/rsync (if you have the SSH add-on)

```bash
rsync -avz --delete custom_components/pantrist/ \
  root@homeassistant.local:/config/custom_components/pantrist/
ssh root@homeassistant.local "ha core restart"
```

## Add the integration

1. **Settings → Devices & Services → + Add Integration**.
2. Search "Pantrist" → click.
3. Browser opens at Pantrist's `/oauth/authorize` page.
4. Log in if needed, pick the list to expose, click **Allow**.
5. Browser returns to HA; entry is created.

You should now see four sensors:

- `sensor.pantrist_shopping_list`
- `sensor.pantrist_pantry`
- `sensor.pantrist_expiring_soon`
- `sensor.pantrist_shopping_cart`

## Iterate

After a code change locally:

```bash
# Samba path:
cp -r custom_components/pantrist /Volumes/config/custom_components/pantrist
# Then in HA: Developer Tools → YAML → Check Configuration → Restart
```

For schema/import errors, **Settings → System → Logs** shows line numbers you
can match against your local files.

## Architecture

Inside `custom_components/pantrist/`:

| Module | Responsibility |
|---|---|
| `manifest.json` | Integration metadata, deps, OAuth declaration |
| `const.py` | DOMAIN, OAuth URLs, sensor + service keys |
| `application_credentials.py` | Provides `LocalOAuth2ImplementationWithPkce` (no client secret) |
| `config_flow.py` | OAuth flow + reauth; stores `list_id` from token response |
| `api.py` | Async aiohttp wrapper over the Pantrist REST API |
| `coordinator.py` | `DataUpdateCoordinator` with REST refresh + Socket.IO push |
| `sensor.py` | Four `SensorEntity` subclasses (shopping list, pantry, expiring, cart) |
| `__init__.py` | `async_setup_entry` / `async_unload_entry` + service registrations |
| `services.yaml` | Service schemas for the HA UI |
| `strings.json` + `translations/{en,de}.json` | i18n |

The OAuth flow uses HA's standard `my.home-assistant.io/redirect/oauth`
trampoline. The Pantrist API's redirect-URI whitelist accepts that host plus
local HA hostnames (`homeassistant.local`, `*.ui.nabu.casa`, RFC1918 IPs).

## Releasing

HACS picks up new versions from GitHub releases.

```bash
# After merging the integration changes to main:
git checkout main
git pull
gh release create v0.1.1 --title "v0.1.1" --notes "..."
```

Users with HACS will see the update within a few minutes.

## Common issues

| Problem | Fix |
|---|---|
| "Pantrist" not appearing in "Add Integration" | Restart HA — `custom_components/` is only scanned at boot. |
| `missing_configuration` | Add the Application Credential (one-time setup above). |
| `invalid_redirect_uri` from Pantrist | The Pantrist API needs `my.home-assistant.io` in its redirect-URI whitelist. |
| OAuth completes but sensors stay `unavailable` | Check HA logs for Socket.IO connection errors. Verify `api.pantrist.app` is reachable from the HA host. |
| `missing_list_id` abort | The Pantrist consent page must include a list picker (Pantrist app deployment must be current). |
