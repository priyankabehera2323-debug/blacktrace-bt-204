import ast
import unittest
from pathlib import Path


class ReviewProcessorTests(unittest.TestCase):
    def test_processor_has_no_shell_execution(self):
        source = Path(
            "target-files/challenge/bin/process-request.py"
        ).read_text()
        tree = ast.parse(source)

        forbidden = {"system", "popen", "exec", "eval"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else ""
                self.assertNotIn(name, forbidden)

    def test_processor_validates_ticket_and_action(self):
        source = Path(
            "target-files/challenge/bin/process-request.py"
        ).read_text()
        self.assertIn(
            "from review_policy import validate_request", source
        )
        policy = Path(
            "target-files/challenge/bin/review_policy.py"
        ).read_text()
        self.assertIn('ticket not in ALLOWED_TICKETS', policy)
        self.assertIn('action not in ALLOWED_ACTIONS', policy)

    def test_proof_setup_is_root_only(self):
        source = Path(
            "target-files/challenge/setup-challenge-state.sh"
        ).read_text()
        self.assertIn("chmod 0600", source)
        self.assertIn("chown root:root", source)


if __name__ == "__main__":
    unittest.main()
