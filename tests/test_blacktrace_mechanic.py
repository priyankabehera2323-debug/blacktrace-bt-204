import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSOR = ROOT / "target-files/challenge/bin/process-request.py"
POLICY = ROOT / "target-files/challenge/bin/review_policy.py"
STATE_SETUP = ROOT / "target-files/challenge/setup-challenge-state.sh"


class BlackTraceMechanicTests(unittest.TestCase):
    def test_processor_uses_review_policy(self):
        source = PROCESSOR.read_text()
        self.assertIn("from review_policy import validate_request", source)

    def test_policy_rejects_unsupported_actions(self):
        source = POLICY.read_text()
        self.assertIn("action not in ALLOWED_ACTIONS", source)

    def test_processor_does_not_execute_shell_commands(self):
        tree = ast.parse(PROCESSOR.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, {"system", "popen", "eval", "exec"})

    def test_setup_protects_root_proof(self):
        source = STATE_SETUP.read_text()
        self.assertIn("chown root:root", source)
        self.assertIn("chmod 0600", source)


if __name__ == "__main__":
    unittest.main()
