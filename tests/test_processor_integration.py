import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
PROCESSOR = PROJECT / "target-files/challenge/bin/process-request.py"


class ProcessorIntegrationTests(unittest.TestCase):
    def run_processor(self, temp_dir, reviewer, action="review", profile=None):
        d = Path(temp_dir)
        inbox = d / "inbox"
        inbox.mkdir(exist_ok=True)

        request = inbox / "request.json"
        request.write_text(json.dumps({
            "ticket": "BT-204",
            "action": action,
            "reviewer": reviewer,
        } | ({"profile": profile} if profile is not None else {})), encoding="utf-8")

        proof = d / "proof.txt"
        proof.write_text(
            "TEST_PROOF_PLACEHOLDER\n", encoding="utf-8"
        )

        report = d / "reports" / "BT-204-review.txt"
        audit = d / "logs" / "review-audit.jsonl"

        env = os.environ.copy()
        env.update({
            "BLACKTRACE_REQUEST": str(request),
            "BLACKTRACE_AUDIT": str(audit),
            "BLACKTRACE_PROOF": str(proof),
            "BLACKTRACE_REPORT": str(report),
        })

        result = subprocess.run(
            [sys.executable, str(PROCESSOR)],
            cwd=PROCESSOR.parent,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        return result, report, audit, request

    def test_valid_profile_check_creates_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, report, audit, request = self.run_processor(
                tmp, "maintenance-operator",
                action="profile-check",
                profile="NIGHTJAR-17",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(report.is_file())
            self.assertIn(
                "profile check complete",
                report.read_text(encoding="utf-8"),
            )

    def test_invalid_profile_check_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, report, audit, request = self.run_processor(
                tmp, "maintenance-operator",
                action="profile-check",
                profile="WRONG-PROFILE",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(report.exists())

    def test_valid_request_creates_report_and_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, report, audit, request = self.run_processor(
                tmp, "maintenance-operator"
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(report.is_file())

            report_text = report.read_text(encoding="utf-8")

            self.assertIn("BlackTrace BT-204 review complete", report_text)
            self.assertIn("Proof: retained in protected storage", report_text)
            self.assertNotIn("TEST_PROOF_PLACEHOLDER", report_text)

            self.assertTrue(audit.is_file())
            self.assertFalse(request.exists())

    def test_unauthorized_reviewer_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, report, audit, request = self.run_processor(
                tmp, "unauthorized-user"
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Rejected:", result.stdout)
            self.assertFalse(report.exists())
            self.assertTrue(request.exists())  # Rejected requests remain pending.
            self.assertFalse(audit.exists())  # Rejection occurs before audit logging.


if __name__ == "__main__":
    unittest.main()
