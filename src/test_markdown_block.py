import unittest

from markdown_block import MDBlock

from markdown_block import block_to_block_type

class TestMarkdownBlock(unittest.TestCase):
    def test_heading_1(self):
        block = "# This is a heading"
        self.assertEqual(MDBlock.HEADING, block_to_block_type(block))

    def test_heading_2(self):
        block = "### This is a heading"
        self.assertEqual(MDBlock.HEADING, block_to_block_type(block))

    def test_heading_too_many_hashes(self):
        block = "####### This is a heading"
        self.assertEqual(MDBlock.PARAGRAPH, block_to_block_type(block))

    def test_heading_with_interference(self):
        block = "### This is a heading with more ###### and even ############"
        self.assertEqual(MDBlock.HEADING, block_to_block_type(block))

    def test_code_1(self):
        block = "```This is some code```"
        self.assertEqual(MDBlock.CODE, block_to_block_type(block))

    def test_code_with_interference(self):
        block = """```This is some code``` but it ends here ```"""
        self.assertEqual(MDBlock.CODE, block_to_block_type(block))

    def test_code_with_not_enough_backticks(self):
        block = """``This is some code```"""
        self.assertEqual(MDBlock.PARAGRAPH, block_to_block_type(block))

    def test_quote(self):
        block = """> This is some quote"""
        self.assertEqual(MDBlock.QUOTE, block_to_block_type(block))
        
    def test_quote_no_space(self):
        block = """>This is some quote"""
        self.assertEqual(MDBlock.QUOTE, block_to_block_type(block))
            
    def test_unord_list(self):
        block = """- item 1
- item 2
- item 3"""
        self.assertEqual(MDBlock.UNORDERED_LIST, block_to_block_type(block))

    def test_unord_list_bad_spacing_but_ok(self):
        block = """- item 1
-item 2
- item 3"""
        self.assertEqual(MDBlock.UNORDERED_LIST, block_to_block_type(block))

    def test_unord_list_bad_list(self):
        block = """-item 1
- item 2
- item 3"""
        self.assertEqual(MDBlock.PARAGRAPH, block_to_block_type(block))

    def test_ord_list(self):
        block = """1. item 1
2. item 2
3. item 3"""
        self.assertEqual(MDBlock.ORDERED_LIST, block_to_block_type(block))

    def test_ord_list_bad_counting(self):
        block = """1. item 1
3. item 2
3. item 3"""
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_ord_list_bad_start(self):
        block = """2. item 1
3. item 2
4. item 3"""
        self.assertEqual(MDBlock.PARAGRAPH, block_to_block_type(block))