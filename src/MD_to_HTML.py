import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_block import MDBlock

from markdown_block import block_to_block_type
from markdown_handler import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes: list[HTMLNode] = []
    for block in blocks:
        block_type: MDBlock = block_to_block_type(block)
        nodes.append(build_html_node(block, block_type))
    return ParentNode('div', nodes)


def build_html_node(block: str, block_type: MDBlock):
    match block_type:
        case MDBlock.PARAGRAPH:
            return ParentNode('p', text_to_children(block))
        case MDBlock.HEADING:
            head: str = list(re.findall(r"^\#{1,6}", block))[0]
            stripped_block: str = block.lstrip("# ")
            return ParentNode(f"h{len(head)}", text_to_children(stripped_block))
        case MDBlock.CODE:
            stripped_block: str = block.strip("`\n")
            return ParentNode("pre", [LeafNode("code", stripped_block)])
        case MDBlock.QUOTE:
            stripped_block: str = "\n".join(re.split(r"\n>", block))
            return ParentNode("blockquote", text_to_children(stripped_block[1:]))
        case MDBlock.UNORDERED_LIST:
            items: list[str] = block[2:].split("\n- ")
            bullet_items: list[HTMLNode] = []
            for item in items:
                bullet_items.append(ParentNode("li", text_to_children(item)))
            return ParentNode("ul", bullet_items)
        case MDBlock.ORDERED_LIST:
            items: list[str] = re.split(r"1\. |\n\d+\. ", block)[1:]
            enum_items: list[HTMLNode] = []
            for item in items:
                enum_items.append(ParentNode("li", text_to_children(item)))
            return ParentNode("ol", enum_items)


def text_to_children(block: str) -> list[HTMLNode]:
    nodes: list[TextNode] = text_to_textnodes(block)
    return [text_node_to_html_node(node) for node in nodes]