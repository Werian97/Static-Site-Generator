from textnode import TextNode, TextType
from re import findall

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes:list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter in node.text:
            pieces = node.text.split(delimiter)
            if len(pieces) % 2 == 0:
                raise Exception("Pheraps a delimiter is missing")
            else:
                nodes_from_pieces: list[TextNode] = []
                for i, piece in enumerate(pieces):
                    if piece != '':
                        if i % 2 == 0:
                            nodes_from_pieces.append(TextNode(piece, TextType.TEXT))
                        else:
                            nodes_from_pieces.append(TextNode(piece, text_type))
                new_nodes.extend(nodes_from_pieces)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes:list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = extract_markdown_images(text)
        for match in matches:
            image_string: str = f"![{match[0]}]({match[1]})"
            pieces = text.split(image_string, 1)
            if pieces[0] != '':
                new_nodes.append(TextNode(pieces[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = pieces[1]
        if text != '':
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes:list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = extract_markdown_links(text)
        for match in matches:
            image_string: str = f"[{match[0]}]({match[1]})"
            pieces = text.split(image_string, 1)
            if pieces[0] != '':
                new_nodes.append(TextNode(pieces[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            text = pieces[1]
        if text != '':
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes