import unittest

from MD_to_HTML import markdown_to_html_node

class TestMDToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_paragraph_with_every_good_of_god(self):
        md = """
Ok, so, here we have **bold** and _italic_, but also ```code```. We didn't stop there! We also have ![image](https://pic) and... no way: a [link](https://linkystuff)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Ok, so, here we have <b>bold</b> and <i>italic</i>, but also <code>code</code>. We didn't stop there! We also have <img alt=\"image\" src=\"https://pic\"> and... no way: a <a href=\"https://linkystuff\">link</a></p></div>"
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item
3. fourth... nahh I'm joking
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>fourth... nahh I'm joking</li></ol></div>"
        )

    def test_unordered_list(self):
        md = """
- first item
- second item
- fourth... nahh I'm joking
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>fourth... nahh I'm joking</li></ul></div>"
        )

    def test_quote(self):
        md = "> Erano i capei d'oro all'aura sparsi"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote> Erano i capei d'oro all'aura sparsi</blockquote></div>"
        )

    def test_heading_and_paragraph(self):
        markdown = """
# Heading

This is a paragraph.
"""

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>This is a paragraph.</p></div>"
        )

    def test_quote_and_code(self):
        markdown = """
> To be
> or not to be

```
print("hello")
```
"""

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            '<div><blockquote> To be\n or not to be</blockquote><pre><code>print("hello")</code></pre></div>'
        )

    def test_mixed_document(self):
        markdown = """
# My title

This is **bold** text.

- One
- Two

```
x = 42
```
"""

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>My title</h1><p>This is <b>bold</b> text.</p><ul><li>One</li><li>Two</li></ul><pre><code>x = 42</code></pre></div>"
        )

    def test_every_block_in_the_book(self):
        markdown = """
# Title

Paragraph with _italic_ and **bold**.

> Quote

- A
- B

1. One
2. Two

```
x = 42
```
"""

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Paragraph with <i>italic</i> and <b>bold</b>.</p><blockquote> Quote</blockquote><ul><li>A</li><li>B</li></ul><ol><li>One</li><li>Two</li></ol><pre><code>x = 42</code></pre></div>"
        )