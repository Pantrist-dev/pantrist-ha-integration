# Changelog

All notable changes to the Pantrist HA Integration are recorded here.
Generated from Conventional Commits by [standard-version](https://github.com/conventional-changelog/standard-version).


### [0.1.2](https://github.com/Pantrist-dev/pantrist-ha-addon/compare/v0.1.1...v0.1.2) (2026-05-27)


### Bug Fixes

* **logo:** add hDPI logo ([b378da3](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/b378da372a194288097ff95bffcc46874116d652))

### [0.1.1](https://github.com/Pantrist-dev/pantrist-ha-addon/compare/v0.1.0...v0.1.1) (2026-05-26)


### Bug Fixes

* **calendar:** display amount correctly ([4188357](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/418835733fd3d231e42535060f39e1a4a4adb8e8))
* **coordinator:** disable socketio internal reconnect to refresh tokens ([0217e02](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/0217e022c3fbdfc8cff090eefae03fc2d79a88e2))
* **pantry-values:** use localized item name ([e52984f](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/e52984f5c49e42eb3cc1a08506ff547380d4d0b0))

## 0.1.0 (2026-05-22)


### Features

* **autoRestock:** wire the per-request flag through HA + NFC blueprint ([4c9c6a2](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/4c9c6a2705a1339662e83ecb541fd46ea450d8f1))
* **barcode-adding:** use new add-by-barcode method ([970df1a](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/970df1a3a7660f9969e2ea6e1b55bf62033abe72))
* **blueprints:** NFC tag → consume pantry item ([f091f09](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/f091f09c54a34ebcb8019b6bd090ce32913aee49))
* **blueprints:** ship 3 ready-to-import blueprints + dashboard card snippet ([a87f7fa](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/a87f7fad6390120e3fd037f7ae8e5ac91bda45c7))
* **config_flow:** use the actual list name as entry title ([de227bf](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/de227bf7a47b9a4fa924043c717ba66db101e325))
* **config-flow:** support reconfigure flow ([6f9f6f9](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/6f9f6f92cf9c6c586eaadae1cb09f815ecbd4066))
* **diagnostics:** per-list status + redacted entry config ([3b5e165](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/3b5e165703b4cbd348eb63289cf4527b6febd73c))
* **entities,coordinator:** pantry-amount number, latest-item image, ([b304def](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/b304defb3b6d9e270bf3116ed5d3212a7393a484))
* **entities:** add binary sensors, next-expiration timestamp, calendar ([c82a123](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/c82a123b76670be0ef65ae446df4bbeefadd4e7f))
* generate Python addon client from OpenAPI spec ([8d8e1ad](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/8d8e1ade83fb83a3e70800b3a901ab7d8a95fc15))
* **ha-addon:** add Credentials persistence module + pytest setup ([b3198ea](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/b3198ea606cce19c46343528676ba6d43883b432))
* **ha-addon:** add ingress UI with OAuth start/callback/disconnect ([eb97598](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/eb97598ba2bfe666ab519aa96552a21de892e37d))
* **ha-addon:** add OAuth PKCE flow ([e55f415](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/e55f4150da0abf35ddbd282116f6adce84a14a5e))
* **ha-addon:** add PantristSession lifecycle wrapper ([bd24726](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/bd24726b568ef644110f50a4b978c65b5d143cd0))
* **ha-addon:** add persistent_notification helper ([78300b8](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/78300b88d502b2b172185a24f4d0fec697e0097f))
* **ha-addon:** enable ingress, remove static-token config keys ([05ce879](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/05ce879ba10c699a1b71b6dc9a8b025418b9f029))
* **ha-addon:** extract aiohttp service server ([e32d581](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/e32d5810fbc21c916138d87d122192f51298757d))
* **ha-addon:** Home Assistant addon for Pantrist ([d4e0482](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/d4e0482242448f5e649ac4251b86864564b9e99f))
* **ha-addon:** on 3 consecutive 401s invoke failure callback ([292167b](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/292167bd7fc902cfe21f39a41102d40e47377ced))
* **ha-addon:** rewrite main.py for two-phase bootstrap ([5eb27a0](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/5eb27a0264486177910b8a396bf03d9db90fd36a))
* **integration:** use generated OpenAPI client + restore barcode/pantry-add services ([3a012f9](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/3a012f9fc61e749709b7876973829d7847f78941))
* **list-manager:** dynamic + stale device handling ([2a096e8](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/2a096e8ed081304750aff33b5e33921d944685c3))
* **list-manager:** push-driven list:added / list:removed + ([2236007](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/2236007acc7cb558f015fbc29bb1824900a97797))
* **list-manager:** socket-driven rename + delete ([760dae1](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/760dae104fdf629d1d4007e47235e753662e536b))
* make the addon findable from HA ([405fbe5](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/405fbe5ce7f275160916f964f95d81b7bd5253b9))
* **multi-list:** one device per Pantrist list, no more per-list OAuth ([3ba1c78](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/3ba1c78c69b5141df1e9e5ca55954f112c2ddbdc))
* **oauth:** pre-register the PKCE implementation — no manual setup ([155a6ef](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/155a6efd2bb2805fb84db838846970f2399bd06b))
* **quality-scale:** close every Bronze tier gap ([ef36abc](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/ef36abc635283e3be53f5af46bfcb23f57472b19))
* **quality-scale:** entity-category + exception-translations ([1c3513a](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/1c3513a04a6d84e084f957ccb985fcac36c2f48b))
* ship brand icons in the integration's brand directory ([9c355c1](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/9c355c1935fff81397dc0c7591b1ed7277c9abff))
* simplify oauth flow ++ display amount string correctly ([5f1556e](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/5f1556e06687c949d29683cb6e7fb35636ab2932))
* **todo:** expose each shopping list as an HA todo entity ([9914cef](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/9914cefc6946e90891113d479c20b697b1e452fb))


### Bug Fixes

* **blueprint:** low_stock_auto_add skips items already on the shopping list ([3e87080](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/3e870806d4f0026f67bdce0b1f7921d4923fd9f2))
* **build:** add build instructions for python ([dbc25e2](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/dbc25e21275f233024ef4a02748bbc2ed8d6e2dd))
* **build:** enerate openapi client ([ba02b00](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/ba02b00c96a389079c6c1b1463a62484e57089e8))
* **build:** regenerate openapi client ([e2d51a2](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/e2d51a2d579931311f042d51529e8f1ab8140aee))
* correct minimum Home Assistant version in hacs.json ([777a560](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/777a560ca1cb904034a258f08ea9b8b8618f30a6))
* **entities:** YYYY-MM-DD best-before format + correct unit semantics ([35f9963](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/35f99637dd3b079ad51dfb59404522d0b03980cb))
* **ha-addon:** align endpoints with actual backend spec; update openapi script URL ([61b049d](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/61b049d4ccebdd7e025acbd5b54dea7a662308e3))
* **integration:** pre-import OAuth client + use display in dashboard card ([40fa475](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/40fa475373c2aac848f7fb84909c47f8a2b02fb0))
* **manifest:** drop httpx + attrs from requirements — HA Core bundles both ([a4a7be2](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/a4a7be263897678d2a75e6f16400f4b3fae8e583))
* **oauth:** consent page URL is www.pantrist.app, not app.pantrist.app ([a82384e](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/a82384eea877ae3ce51c45aa04c2d97d8e6d45d7))


### Refactoring

* **api:** use typed DTO parsing now that generator is patched ([6d051f2](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/6d051f2f363cbae26a5ee2dd67f2445e6d6d63a0))
* **coordinator:** drop the 5-min poll, refresh on socket reconnect ([19632d8](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/19632d841d7a8e6a1fa6e53258d1095825f80084))
* replace Docker Add-on with Custom Integration ([8ff6d68](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/8ff6d688643f25d6374afd8438f6f3830df381b0))


### Documentation

* capture multi-list, todo, blueprints, removal + mypy workflow ([3e7e348](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/3e7e348e6e6792e91835c9598f4ca8e45e7ff528))
* cover binary sensors, calendar, next-expiration, reconfigure, ([290f1fa](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/290f1fa43913ec3a989fd7f6253278e11388dc13))
* explicit 'add the To-do list card' walkthrough ([67c8296](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/67c82965d856b2e7817d36f260f2d02ec8306e64))
* **ha-addon:** rewrite for OAuth flow ([bde4319](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/bde4319d1a9d3d2cc25077c732a711a5fa51a7d5))
* switch documentation to English ([4fe8986](https://github.com/Pantrist-dev/pantrist-ha-addon/commit/4fe898673f2ffd2fbc43561410e4c42ea7200d89))
