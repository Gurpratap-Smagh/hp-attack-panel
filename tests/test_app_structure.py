import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class MockResponse:
    status_code = 204


class MockAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def request(self, *args, **kwargs):
        return MockResponse()


class AppStructureTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_index_served_from_frontend(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("hp-attack-panel", response.text)
        self.assertIn('src="/static/app.js"', response.text)

    @patch("backend.services.attack.httpx.AsyncClient", MockAsyncClient)
    @patch(
        "backend.services.attack.load_payloads",
        return_value=[
            {
                "id": "p-test",
                "name": "Test payload",
                "method": "GET",
                "path": "/health",
                "headers": {},
                "body": "",
            }
        ],
    )
    def test_fire_random_endpoint_uses_backend_services(self, _mock_load_payloads):
        response = self.client.post("/fire-random")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["payload_id"], "p-test")
        self.assertEqual(body["target_url"], "http://localhost:8080/health")
        self.assertEqual(body["status_code"], 204)


if __name__ == "__main__":
    unittest.main()
