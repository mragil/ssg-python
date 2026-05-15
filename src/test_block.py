import unittest
from block import block_to_block_type, BlockType

class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()