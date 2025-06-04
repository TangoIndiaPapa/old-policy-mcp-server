import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from server import PolicyMCPServer

class TestPolicyMCPServer(unittest.TestCase):
    def setUp(self):
        self.server = PolicyMCPServer()

    def test_waldo_blocked(self):
        result = self.server.enforce_policy("where is waldo?")
        self.assertEqual(result['result'], 'not compliant')
        self.assertIn('test', result['reason'].lower())

    def test_carmen_allowed(self):
        result = self.server.enforce_policy("where is carmen sandiego?")
        self.assertEqual(result['result'], 'compliant')

if __name__ == "__main__":
    unittest.main()
