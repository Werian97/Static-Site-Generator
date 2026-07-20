import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("some text", TextType.LINK, "https://randomlink")
        self.assertEqual("TextNode(some text, link, https://randomlink)", str(node))
    
    def test_noteq1(self):
        node = TextNode("some text", TextType.LINK, "https://randomlink")
        node2 = TextNode("sometext", TextType.LINK, "https://randomlink")
        self.assertNotEqual(node, node2)
    
    def test_noteq2(self):
        node = TextNode("some text", TextType.LINK, "https://randomlink")
        node2 = TextNode("some text", TextType.IMAGE, "https://randomlink")
        self.assertNotEqual(node, node2)

    def test_noteq3(self):
        node = TextNode("some text", TextType.LINK, "https://randomlink")
        node2 = TextNode("some text", TextType.LINK, "https://randomlin")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()