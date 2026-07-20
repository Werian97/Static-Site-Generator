from textnode import TextNode, TextType

def main():
    node = TextNode("let's try something", TextType.IMAGE, "/gattini.png")
    print(node)

main()