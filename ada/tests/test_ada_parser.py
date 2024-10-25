# Unit tests for Ada parser

import unittest
from ada.parser import Parser

class TestAdaParser(unittest.TestCase):
    def test_parse_simple_function(self):
        parser = Parser()
        self.assertEqual(parser.parse("function main is"), "main")
