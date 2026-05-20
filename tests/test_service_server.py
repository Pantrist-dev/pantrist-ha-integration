import pytest
from aiohttp.test_utils import TestClient, TestServer


class FakeAPI:
    def __init__(self):
        self.calls = []

    def add_to_shopping_list_by_name(self, name):
        self.calls.append(("add", name))
        return {"id": "x"}

    def add_to_shopping_list_by_barcode(self, barcode):
        self.calls.append(("add_barcode", barcode))
        return {"id": "y"}

    def add_to_pantry_by_name(self, list_id, name, amount, unit_id):
        self.calls.append(("add_pantry", list_id, name, amount, unit_id))
        return {"id": "p"}

    def check_shopping_list_item(self, item_id):
        self.calls.append(("check", item_id))

    def delete_shopping_list_item(self, list_id, item_id):
        self.calls.append(("delete_shop", list_id, item_id))

    def delete_pantry_item(self, list_id, item_id):
        self.calls.append(("delete_pantry", list_id, item_id))

    def change_pantry_item_amount(self, list_id, item_id, change, unit_id):
        self.calls.append(("change", list_id, item_id, change, unit_id))


@pytest.mark.asyncio
async def test_health():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.get("/health")
        assert resp.status == 200
        assert await resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_add_to_shopping_list_dispatches():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/services/add_to_shopping_list", json={"name": "Milk"}
        )
        assert resp.status == 200
        assert api.calls == [("add", "Milk")]


@pytest.mark.asyncio
async def test_add_to_shopping_list_by_barcode_dispatches():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/services/add_to_shopping_list_by_barcode",
            json={"barcode": "4006381333931"},
        )
        assert resp.status == 200
        assert api.calls == [("add_barcode", "4006381333931")]


@pytest.mark.asyncio
async def test_check_shopping_list_item_dispatches():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/services/check_shopping_list_item", json={"item_id": "abc"}
        )
        assert resp.status == 200
        assert api.calls == [("check", "abc")]


@pytest.mark.asyncio
async def test_change_pantry_amount_dispatches():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/services/change_pantry_item_amount",
            json={
                "list_id": "list-1",
                "item_id": "i-1",
                "change": -1,
                "unit_id": "pieces",
            },
        )
        assert resp.status == 200
        assert api.calls == [("change", "list-1", "i-1", -1.0, "pieces")]


@pytest.mark.asyncio
async def test_returns_503_when_session_not_started():
    from service_server import make_service_app

    app = make_service_app(api_provider=lambda: None)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post(
            "/services/add_to_shopping_list", json={"name": "Milk"}
        )
        assert resp.status == 503


@pytest.mark.asyncio
async def test_unknown_path_returns_404():
    from service_server import make_service_app

    api = FakeAPI()
    app = make_service_app(api_provider=lambda: api)
    async with TestClient(TestServer(app)) as client:
        resp = await client.post("/services/unknown_endpoint", json={})
        assert resp.status == 404
