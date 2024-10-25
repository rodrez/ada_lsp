# Unit tests for JSON-RPC communication

import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import AdaLSPServer

class TestJSONRPC(unittest.TestCase):
    def setUp(self):
        self.server = AdaLSPServer()

    def tearDown(self):
        self.server.close()

    def test_completion(self):
        result = self.server.complete("main")
        self.assertIsInstance(result, list)
        self.assertIn("main", result)

    def test_empty_completion(self):
        result = self.server.complete("")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_invalid_completion(self):
        result = self.server.complete("xyzabc")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_initialize(self):
        result = self.server.initialize({"rootUri": "./"})
        self.assertIsInstance(result, dict)
        self.assertIn("capabilities", result)

    def test_shutdown(self):
        result = self.server.shutdown()
        self.assertIsNone(result)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.server.exit()

if __name__ == '__main__':
    unittest.main()
