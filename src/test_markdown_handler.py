import unittest
from textnode import TextNode, TextType

from markdown_handler import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_noTEXTtype_ignored_1(self):
        node = TextNode("This is a **bold** text node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(1, len(new_nodes))
        new_node = new_nodes[0]
        self.assertEqual(node, new_node)
    
    def test_noTEXTtype_ignored_2(self):
        node = TextNode("This is a **bold** text node", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(1, len(new_nodes))
        new_node = new_nodes[0]
        self.assertEqual(node, new_node)

    def test_noTEXTtype_ignored_3(self):
        node1 = TextNode("This is a **bold** text node", TextType.BOLD)
        node2 = TextNode("This is another text node, but italic", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.ITALIC)
        self.assertEqual(2, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]
        self.assertEqual(node1, new_node1)
        self.assertEqual(node2, new_node2)
    
    def test_ignore_when_delimiter_not_found(self):
        node1 = TextNode("There is some **bold text** in this node", TextType.TEXT)
        node2 = TextNode("There is even some _italic text_ in this node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(2, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]
        self.assertEqual(node1, new_node1)
        self.assertEqual(node2, new_node2)
    
    def test_normal_behaviour_one_node(self):
        node = TextNode("There is some `code` in this node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(3, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]
        new_node3 = new_nodes[2]

        self.assertEqual(TextNode("There is some ", TextType.TEXT),
                    new_node1)
        self.assertEqual(TextNode("code", TextType.CODE),
                    new_node2)
        self.assertEqual(TextNode(" in this node", TextType.TEXT),
                    new_node3)
    
    def test_missing_closing_delimiter(self):
        node = TextNode("Oh no, where `is the second backtic?", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimiter(self):
        node = TextNode("Here's some `code` and here is some `other code`. Magnificent!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(5, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]
        new_node3 = new_nodes[2]
        new_node4 = new_nodes[3]
        new_node5 = new_nodes[4]

        self.assertEqual(TextNode("Here's some ", TextType.TEXT),
                    new_node1)
        self.assertEqual(TextNode("code", TextType.CODE),
                    new_node2)
        self.assertEqual(TextNode(" and here is some ", TextType.TEXT),
                    new_node3)
        self.assertEqual(TextNode("other code", TextType.CODE),
                    new_node4)
        self.assertEqual(TextNode(". Magnificent!", TextType.TEXT),
                    new_node5)
    
    def test_edge_delimiters(self):
        node1 = TextNode("**We start bold** but we finish plain", TextType.TEXT)
        node2 = TextNode("We start plain **but we finish bold**", TextType.TEXT)
        node3 = TextNode("**EVERYTHING IS BOLD HERE**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertEqual(5, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]
        new_node3 = new_nodes[2]
        new_node4 = new_nodes[3]
        new_node5 = new_nodes[4]

        self.assertEqual(TextNode("We start bold", TextType.BOLD),
                    new_node1)
        self.assertEqual(TextNode(" but we finish plain", TextType.TEXT),
                    new_node2)
        self.assertEqual(TextNode("We start plain ", TextType.TEXT),
                    new_node3)
        self.assertEqual(TextNode("but we finish bold", TextType.BOLD),
                    new_node4)
        self.assertEqual(TextNode("EVERYTHING IS BOLD HERE", TextType.BOLD),
                    new_node5)

    def test_nested_calls(self):
        node = TextNode("Here is some _italic_ text and some **bold** text. There's even some _more italic_ here", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(5, len(new_nodes))
        self.assertEqual(TextNode(" text and some **bold** text. There's even some ", TextType.TEXT), new_nodes[2])
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(7, len(new_nodes))
    
    def test_close_equal_delimiters(self):
        node = TextNode("**bold**** next to bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(2, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]

        self.assertEqual(TextNode("bold", TextType.BOLD),
                    new_node1)
        self.assertEqual(TextNode(" next to bold", TextType.BOLD),
                    new_node2)

    def test_close_different_delimiters(self):
        node = TextNode("**bold**_ next to italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(2, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]

        self.assertEqual(TextNode("bold", TextType.BOLD),
                    new_node1)
        self.assertEqual(TextNode("_ next to italic_", TextType.TEXT),
                    new_node2)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(2, len(new_nodes))
        new_node1 = new_nodes[0]
        new_node2 = new_nodes[1]

        self.assertEqual(TextNode("bold", TextType.BOLD),
                    new_node1)
        self.assertEqual(TextNode(" next to italic", TextType.ITALIC),
                    new_node2)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://maliciouslink)"
        )
        self.assertListEqual([("link", "https://maliciouslink")], matches)
        
    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a first [link](https://maliciouslink) and then a second [other](https://moremaliciouslink)"
        )
        self.assertListEqual([("link", "https://maliciouslink"),
                              ("other", "https://moremaliciouslink")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a first ![image](https://i.imgur.com/zjjcJKZ.png) and then a second ![picture](https://jibberish.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),
                              ("picture", "https://jibberish.png")], matches)

    def test_extract_images_ignore_links(self):
        matches = extract_markdown_images(
            "This is text with a first ![image](https://i.imgur.com/zjjcJKZ.png) and then a second [link](https://malicious)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_links_ignore_images(self):
        matches = extract_markdown_links(
            "This is text with a first ![image](https://i.imgur.com/zjjcJKZ.png) and then a second [link](https://malicious)"
        )
        self.assertListEqual([("link", "https://malicious")], matches)
    
    def test_ignore_miswritten_images(self):
        matches = extract_markdown_images(
            "This is text with a broken ![image[image](/folder/directory/cats.png)"
        )
        self.assertListEqual([], matches)
    
    def test_ignore_miswritten_links(self):
        matches = extract_markdown_links(
            "This is text with a broken [link[link]](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_the_same_image_twice(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another copy of the same ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another copy of the same ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_links_and_images(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png) too",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" too", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes)