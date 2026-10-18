import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "ri", "target-files/app/request-interface.py"
)
ri = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ri)


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ri.INBOX = Path(self.tmp.name) / "inbox"
        self.client = ri.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_health(self):
        self.assertEqual(self.client.get("/health").status_code, 200)

    def test_valid_profile_check(self):
        response = self.client.post(
            "/submit",
            json={
                "ticket": "BT-204",
                "action": "profile-check",
                "profile": "NIGHTJAR-17",
                "reviewer": "maintenance-operator",
            },
        )
        self.assertEqual(response.status_code, 202)

    def test_invalid_profile_check(self):
        response = self.client.post(
            "/submit",
            json={
                "ticket": "BT-204",
                "action": "profile-check",
                "profile": "WRONG-PROFILE",
                "reviewer": "maintenance-operator",
            },
        )
        self.assertEqual(response.status_code, 403)


    def test_valid_request(self):
        r = self.client.post(
            "/submit", json={"ticket": "BT-204", "action": "review"}
        )
        self.assertEqual(r.status_code, 202)
        self.assertTrue((ri.INBOX / "request.json").exists())

    def test_reviewer_field_is_preserved(self):
        r = self.client.post(
            "/submit",
            json={
                "ticket": "BT-204",
                "action": "review",
                "reviewer": "maintenance-operator",
            },
        )
        self.assertEqual(r.status_code, 202)
        import json
        saved = json.loads((ri.INBOX / "request.json").read_text())
        self.assertEqual(saved["reviewer"], "maintenance-operator")

    def test_non_string_reviewer_is_rejected(self):
        r = self.client.post(
            "/submit",
            json={
                "ticket": "BT-204",
                "action": "review",
                "reviewer": ["maintenance-operator"],
            },
        )
        self.assertEqual(r.status_code, 400)

    def test_bad_ticket(self):
        r = self.client.post(
            "/submit", json={"ticket": "BT-999", "action": "review"}
        )
        self.assertEqual(r.status_code, 400)

    def test_bad_action(self):
        r = self.client.post(
            "/submit", json={"ticket": "BT-204", "action": "delete"}
        )
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
