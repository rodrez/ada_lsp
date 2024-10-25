# Unit tests for the completion logic

import unittest
from ada.lsp.completion import CompletionEngine

class TestCompletion(unittest.TestCase):
    def setUp(self):
        self.engine = CompletionEngine()

    def test_basic_completion(self):
        self.assertEqual(self.engine.complete("pro"), ["procedure", "process", "program"])

    def test_no_completion(self):
        self.assertEqual(self.engine.complete("xyz"), [])

    def test_case_sensitivity(self):
        self.assertEqual(self.engine.complete("Pro"), ["procedure", "process", "program"])

    def test_empty_input(self):
        self.assertEqual(self.engine.complete(""), ["procedure", "process", "program"])

    def test_full_word(self):
        self.assertEqual(self.engine.complete("procedure"), ["procedure"])

if __name__ == '__main__':
    unittest.main()
