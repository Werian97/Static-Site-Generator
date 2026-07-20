class HTMLNode():
    def __init__(self, tag: str | None = None,
                 value: str | None = None,
                 children: "list[HTMLNode] | None" = None,
                 props: dict[str, str] | None = None):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: "list[HTMLNode] | None" = children
        self.props: dict[str, str] | None = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        formatted_string: str = ""
        for key in sorted(self.props):
            formatted_string = f'{formatted_string} {key}="{self.props[key]}"'
        return formatted_string
    
    def __repr__(self):
        if self.children is None or self.children == []:
            return f"==========================\n\
tag: {self.tag}\n\
value: {self.value}\n\
children: {None}\n\
props: {self.props}\n\
=========================="
        else:
            children_string = "--------------------------\n"
            for child in self.children:
                children_string = f"{children_string}{child}\n"
            children_string = f"{children_string}--------------------------"
            return f"==========================\n\
tag: {self.tag}\n\
value: {self.value}\n\
children: \n{children_string}\n\
props: {self.props}\n\
=========================="
    
    def __eq__(self, other):
        return (self.tag == other.tag and
        self.value == other.value and
        self.children == other.children and
        self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("No value providedfor leaf node")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag provided for parent node")
        if self.children is None:
            raise ValueError("No children provided for parent node")
        html_text = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_text = f"{html_text}{child.to_html()}"
        html_text = f"{html_text}</{self.tag}>"
        return html_text