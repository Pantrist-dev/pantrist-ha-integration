# Security policy

## Reporting a vulnerability

Please **do not** open a public issue for security bugs.

Email **info@pantrist.app** with:

- a short description of the issue,
- steps to reproduce (or a proof of concept),
- the affected integration version and your Home Assistant version,
- whether the vulnerability is already public.

You should get an acknowledgement within **5 working days**. For confirmed
issues we aim to ship a fix within **30 days**; critical issues get an
out-of-band release pushed to HACS.

## Scope

In scope:

- Credential leaks (OAuth tokens or API keys surfacing in logs, diagnostics
  downloads, or state attributes),
- Crashes or hangs caused by responses from the Pantrist backend or the
  Socket.IO stream,
- Anything that lets one Home Assistant user read or modify another user's
  Pantrist data.

Out of scope:

- Bugs in Home Assistant itself — please report those to
  <https://github.com/home-assistant/core>.
- Bugs in the Pantrist backend — please report those to
  <info@pantrist.app> directly; they are not part of this integration.
- HACS issues unrelated to this integration — please report to
  <https://github.com/hacs/integration>.

## Supported versions

Only the latest release on HACS is actively supported. Older versions
receive fixes only for critical issues.
