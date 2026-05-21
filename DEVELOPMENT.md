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
   - Client Secret: type any placeholder (e.g. `unused`). The Home Assistant
     UI marks this field as required, but Pantrist uses PKCE — the integration
     hard-codes an empty secret internally and ignores the value you enter.
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
# Samba path — verify the file you care about really got copied:
cp -r custom_components/pantrist /Volumes/config/custom_components/
grep OAUTH2_AUTHORIZE /Volumes/config/custom_components/pantrist/const.py
```

Then **fully restart Home Assistant**: Settings → System → **Restart Home
Assistant** (the "Check Configuration" button only validates YAML — it does
NOT reload Python modules under `custom_components/`. A real restart is
required after any code change.)

For faster iteration on a single file, you can also delete the integration
entry (Settings → Devices & Services → Pantrist → ⋮ → Delete), restart,
then re-add it — this clears any cached config_entry state.

For schema/import errors, **Settings → System → Logs** shows line numbers you
can match against your local files.

## Architecture

Inside `custom_components/pantrist/`:

| Module | Responsibility |
|---|---|
| `manifest.json` | Integration metadata, deps, OAuth declaration |
| `const.py` | DOMAIN, OAuth URLs, sensor + service keys |
| `application_credentials.py` | Provides `LocalOAuth2ImplementationWithPkce` (no client secret) |
| `config_flow.py` | OAuth flow + reauth + reconfigure; runs `test-before-configure` against `/list` and stores the chosen `list_id` |
| `api.py` | Async wrapper over the generated OpenAPI client; translates 401 → `PantristAuthError`, other HTTP/network failures → `PantristApiError` |
| `coordinator.py` | One `DataUpdateCoordinator` *per list*: 5-min REST poll fallback + Socket.IO push subscription with exponential reconnect backoff |
| `list_manager.py` | Owns the per-list coordinators, schedules a 5-min reconcile against `GET /list`, dispatches `signal_new_list` for additions and removes HA devices for deletions (Gold: dynamic-devices + stale-devices) |
| `entity.py` | `PantristEntity` base — sets `_attr_has_entity_name`, `device_info` (one HA device per Pantrist list) |
| `sensor.py` | Five sensor classes per list (shopping list, pantry, expiring, cart counts + `next_expiration` timestamp) |
| `binary_sensor.py` | Three binary sensors per list (low_stock, has_expired_items, shopping_list_has_items) |
| `calendar.py` | `PantristPantryCalendar` — pantry items as all-day events on their best-before date |
| `todo.py` | `PantristShoppingTodoEntity` — native HA todo entity wired to add/check/delete shopping-list API calls |
| `diagnostics.py` | `async_get_config_entry_diagnostics` with redacted tokens |
| `__init__.py` | `async_setup` (services, available pre-entry) + `async_setup_entry` (builds the list manager) + `async_unload_entry` |
| `services.yaml` | Service schemas for the HA UI |
| `strings.json` + `translations/{en,de}.json` | i18n |
| `quality_scale.yaml` | Bronze-tier checklist (every Bronze rule is `done`) |
| `pantrist_client/` | **Auto-generated** OpenAPI client. Do not hand-edit — regenerate via `python scripts/generate_client.py` |

The OAuth flow uses HA's standard `my.home-assistant.io/redirect/oauth`
trampoline. The Pantrist API's redirect-URI whitelist accepts that host plus
local HA hostnames (`homeassistant.local`, `*.ui.nabu.casa`, RFC1918 IPs).

### Multi-list mode + dynamic devices

Each Pantrist account can hold multiple lists. The integration runs a single
OAuth flow per account, then creates one HA device *per list* — with five
sensors, three binary sensors, a calendar entity and a todo entity each.
Entries created before multi-list support are migrated in-place: the legacy
`CONF_LIST_ID` in the entry data continues to scope the entry to a single
list, preserving entity IDs.

`PantristListManager` reconciles the live coordinator set against
`GET /list` every five minutes. When the user creates a list in the Pantrist
mobile app, `list_manager` emits the dispatcher signal `signal_new_list(entry_id)`
on the next reconcile and every platform (`sensor`, `binary_sensor`, `calendar`,
`todo`) responds by calling its captured `async_add_entities` for the new
coordinator. When a list is deleted, the manager stops the coordinator,
calls `device_registry.async_remove_device(...)` for `(DOMAIN, list_id)`,
and HA cascades that down to all entities under the device.

The seven action services accept an optional `list_id` field that routes the
call to a specific coordinator. Single-list users can omit it; the integration
falls back to the only available list.

### Blueprints

`blueprints/automation/pantrist/` ships three pre-wired automations
(voice add, low-stock auto-add, expiring notification). They live alongside
the integration so users can import them straight from the GitHub URLs in the
README. Each blueprint declares its own inputs (target todo entity, notify
service, etc.) so users don't have to write any YAML to make them work.

## Tests + type-checking

The integration ships with `pytest-homeassistant-custom-component`-based
tests and is mypy-strict across the modules we own:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

pytest                          # full suite
pytest --cov --cov-report=term  # with line coverage
pytest tests/test_sensor.py     # single file
pytest -k "todo and not auth"   # filtered

mypy                            # strict on integration code (see mypy.ini)
```

The `.coveragerc` excludes the auto-generated `pantrist_client/` from coverage
totals — we don't ship integration tests against the live API, so generated
code lives behind the `api.py` adapter and stays out of the coverage signal.
`mypy.ini` likewise ignores the generated client for strict checks but still
verifies that every cross-reference into it from `api.py` resolves — that's
how the `.asyncio` vs `.asyncio_detailed` attribute mismatch on void
endpoints was originally caught.

Current coverage: **>95% lines + branches** across `__init__.py`,
`api.py`, `application_credentials.py`, `config_flow.py`, `const.py`,
`coordinator.py`, `diagnostics.py`, `entity.py`, `sensor.py`, `todo.py`.

### Regenerating the OpenAPI client

```bash
python scripts/generate_client.py
```

The post-process step inside that script patches two known
`openapi-python-client` 0.28.x bugs (nullable nested `$ref`, empty-string
enums). Re-running it is idempotent.

## Releasing

The repo uses [`standard-version`](https://github.com/conventional-changelog/standard-version) to bump versions, generate `CHANGELOG.md`, and tag releases from Conventional Commits. HACS picks up new versions from the resulting GitHub release tags.

### One-time setup (per machine)

```bash
npm install
```

This installs `standard-version` + `@commitlint/config-conventional` into `node_modules/` (gitignored).

### Cut a release

```bash
git checkout main
git pull

# Inspect what would change without writing anything:
npm run release:dry

# Cut the release: bumps version in package.json + custom_components/pantrist/manifest.json,
# regenerates CHANGELOG.md from Conventional Commits, creates an annotated tag.
npm run release

# Push commits + tag together. HACS sees the new tag and offers the update to users.
git push --follow-tags origin main
```

For the very first release (no previous tag), pass `--first-release` so the
version is committed without auto-incrementing:

```bash
npm run release:first
git push --follow-tags origin main
```

### Optional: create a GitHub Release page from the tag

Tags are enough for HACS, but the GitHub Releases UI gives you nicer release
notes. After pushing the tag:

```bash
gh release create v$(node -p "require('./package.json').version") \
  --title "v$(node -p "require('./package.json').version")" \
  --notes-from-tag
```

### Conventional Commits cheat sheet

| Prefix | When | Bumps |
|---|---|---|
| `feat:` | new feature | minor (0.1.0 → 0.2.0) |
| `fix:` | bug fix | patch (0.1.0 → 0.1.1) |
| `perf:`/`refactor:`/`docs:` | non-feature changes | patch |
| `feat!:` or footer `BREAKING CHANGE:` | breaking API change | major (0.1.0 → 1.0.0) |
| `chore:`/`test:`/`ci:`/`build:` | tooling, no release impact | hidden from changelog |

Commitlint runs at commit time (after installing `husky` if/when added) and
enforces this format.

## Common issues

| Problem | Fix |
|---|---|
| "Pantrist" not appearing in "Add Integration" | Restart HA — `custom_components/` is only scanned at boot. |
| `missing_configuration` | Add the Application Credential (one-time setup above). |
| `invalid_redirect_uri` from Pantrist | The Pantrist API needs `my.home-assistant.io` in its redirect-URI whitelist. |
| OAuth completes but sensors stay `unavailable` | Check HA logs for Socket.IO connection errors. Verify `api.pantrist.app` is reachable from the HA host. |
| `missing_list_id` abort | The Pantrist consent page must include a list picker (Pantrist app deployment must be current). |
