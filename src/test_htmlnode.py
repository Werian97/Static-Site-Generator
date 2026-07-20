import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>")
        node2 = HTMLNode("<p>", None, None, None)
        self.assertEqual(node, node2)

    
    def test_props_to_html1(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html2(self):
        node = HTMLNode("<a>", None, [], {
    "href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_children_dont_interfere(self):
        node1 = HTMLNode()
        node2 = HTMLNode("<a>", None, [], {
    "href": "https://www.google.com",
    "target": "_blank",
})
        node = HTMLNode("<p>",
                "this text should be in a paragraph",
                [node1, node2],
                {"alt": "gattini", "url": "https://gattinid2e22sd3rg56hfd"})
        self.assertEqual(node.props_to_html(), ' alt="gattini" url="https://gattinid2e22sd3rg56hfd"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Visit this site", {"href": "https://www.w3schools.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.w3schools.com">Visit this site</a>')
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "bold text for bald guys")
        self.assertEqual(node.to_html(), '<b>bold text for bald guys</b>')
    
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_withchildren(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    [
                        LeafNode("title", "Why Frontend Development Sucks")
                    ]
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        LeafNode("p", 'Look, front-end development is for script kiddies and soydevs who can\'t \
handle the real programming. I mean, it\'s just a bunch of divs and spans, right? And css??? It\'s like, "Oh, I \
want this to be red, but not thaaaaat red". What a joke.'),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, 'Real programmers code, not silly markup languages. \
They code on Arch Linux, not macOS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the '),
                                LeafNode("a", "backend", {"href": "https://www.boot.dev"}),
                                LeafNode(None, ', where the real programming happens.')
                            ]
                        )
                    ]
                )
            ],
        )
        self.assertEqual(node.to_html(),
                         "<html><head><title>Why Frontend Development Sucks</title></head><body><h1>Front-end Development is the Worst</h1>\
<p>Look, front-end development is for script kiddies and soydevs who can't handle the real programming. I mean, it's just a bunch of divs and spans, \
right? And css??? It's like, \"Oh, I want this to be red, but not thaaaaat red\". What a joke.</p>\
<p>Real programmers code, not silly markup languages. They code on Arch Linux, not macOS, and certainly not Windows. They use Vim, not VS Code. \
They use C, not HTML. Come to the <a href=\"https://www.boot.dev\">backend</a>, where the real programming happens.</p></body></html>")