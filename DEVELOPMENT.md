# Development Guide

## Repository structure

```
pantrist-ha-addon/
├── repository.yaml          # HA addon repository metadata
├── README.md                # User-facing docs
├── DEVELOPMENT.md           # This file
└── pantrist/                # The addon itself
    ├── config.yaml          # Addon metadata (version, arch, options schema)
    ├── build.yaml           # Base images per architecture
    ├── Dockerfile
    ├── DOCS.md              # Shown in HA addon store
    ├── CHANGELOG.md
    ├── logo.png             # 512×512 store banner
    ├── icon.png             # 128×128 tile icon
    ├── requirements.txt
    └── app/
        ├── main.py          # Entrypoint — starts ingress UI + service server
        ├── ingress_server.py
        ├── service_server.py
        ├── pantrist_session.py
        ├── pantrist_api.py  # Thin wrapper around the generated client
        ├── pantrist_client/ # Generated — do not edit by hand (see below)
        ├── oauth_flow.py
        ├── token_manager.py
        ├── ha_integration.py
        ├── credentials.py
        └── templates/
            └── status.html
```

## Generated API client

`app/pantrist_client/` is generated from the Pantrist OpenAPI spec using
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client).
**Do not edit it by hand.**

### Regenerating

1. Make sure a Pantrist API server is running locally on port 3002 (`pnpm start:dev` in `pantrist-api/`), or that `openapi-watch.yaml` in the repo root is up to date.

2. Install the generator (one-time):
   ```bash
   pip install openapi-python-client
   ```

3. From the root of this repo, run:
   ```bash
   # From cached spec (fastest — requires openapi-watch.yaml to exist):
   python scripts/generate_client.py --skip-download

   # Or fetch a fresh spec from the local API (pantrist-api must be running on :3002):
   python scripts/generate_client.py --url http://localhost:3002/swagger-ui-yaml

   # Or fetch from production:
   python scripts/generate_client.py
   ```

4. Commit `pantrist/app/pantrist_client/`.

## Testing locally (without a real HA)

Run the addon directly in Python to verify startup and imports:

```bash
cd pantrist-ha-addon/pantrist
pip install -r requirements.txt
# Create a minimal options file
mkdir -p /data && echo '{"socket_url":"https://api.pantrist.app","expiry_warning_days":7,"custom_ha_url":""}' > /data/options.json
python app/main.py
# Ingress UI available at http://localhost:8100
# Service API available at http://localhost:8099
```

## Releasing a new version

1. Bump `version` in `pantrist/config.yaml`.
2. Add an entry to `pantrist/CHANGELOG.md` matching the new version.
3. Regenerate the API client if the API changed (see above).
4. Commit and push to `main`.
5. In Home Assistant, go to **Settings → Add-ons → Add-on Store → ⋮ → Check for updates**, then reinstall.
