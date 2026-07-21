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
    return findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)