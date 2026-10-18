import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path("target-files/challenge/bin").resolve())
)
from review_policy import validate_request


class ReviewPolicyTests(unittest.TestCase):
    def test_valid_reviewer_is_accepted(self):
        allowed, _ = validate_request({
            "ticket": "BT-204",
            "action": "review",
            "reviewer": "maintenance-operator",
        })
        self.assertTrue(allowed)

    def test_valid_profile_check(self):
        from review_policy import validate_request

        valid, message = validate_request({
            "ticket": "BT-204",
            "action": "profile-check",
            "reviewer": "maintenance-operator",
            "profile": "NIGHTJAR-17",
        })
        self.assertTrue(valid, message)

    def test_invalid_profile_check(self):
        from review_policy import validate_request

        valid, message = validate_request({
            "ticket": "BT-204",
            "action": "profile-check",
            "reviewer": "maintenance-operator",
            "profile": "WRONG-PROFILE",
        })
        self.assertFalse(valid)

    def test_wrong_reviewer_is_rejected(self):
        allowed, _ = validate_request({
            "ticket": "BT-204",
            "action": "review",
            "reviewer": "unknown-user",
        })
        self.assertFalse(allowed)

    def test_wrong_ticket_is_rejected(self):
        allowed, _ = validate_request({
            "ticket": "BT-999",
            "action": "review",
            "reviewer": "maintenance-operator",
        })
        self.assertFalse(allowed)

    def test_unsupported_action_is_rejected(self):
        allowed, _ = validate_request({
            "ticket": "BT-204",
            "action": "root",
            "reviewer": "maintenance-operator",
        })
        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main()
