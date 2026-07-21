import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD, "https://this-link-should-be-ignored")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.props, None)
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC, "https://this-link-should-be-ignored")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.props, None)
    
    def test_code(self):
        node = TextNode("This is some Java code.js", TextType.CODE, "https://this-link-should-be-ignored")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is some Java code.js")
        self.assertEqual(html_node.props, None)
    
    def test_link(self):
        node = TextNode("Emanuele", TextType.LINK, "https://github.com/Werian97")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "Emanuele")
        self.assertEqual(type(html_node.props), dict)
        if type(html_node.props) is dict:
            self.assertEqual(html_node.props["href"], "https://github.com/Werian97")
            self.assertEqual(len(html_node.props), 1)
    
    def test_image(self):
        node = TextNode("gattini meravigliosi!", TextType.IMAGE, "/immagini_segrete/vergogna/gattini_dolcissimi.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(type(html_node.props), dict)
        if type(html_node.props) is dict:
            self.assertEqual(html_node.props["alt"], "gattini meravigliosi!")
            self.assertEqual(html_node.props["src"], "/immagini_segrete/vergogna/gattini_dolcissimi.png")
            self.assertEqual(len(html_node.props), 2)
    
    def test_invalid_type(self):
        node = TextNode("bad node", "not_a_real_type") #type: ignore
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    


if __name__ == "__main__":
    unittest.main()