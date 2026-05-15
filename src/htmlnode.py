from textnode import TextType

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented for HTMLNode")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        print(f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})")

    def text_node_to_html_node(text_node):
        Text_Type_Node_HTML = {
          TextType.TEXT: lambda: LeafNode(None, text_node.text),
          TextType.BOLD: lambda: LeafNode("b", text_node.text),
          TextType.ITALIC: lambda: LeafNode("i", text_node.text),
          TextType.CODE: lambda: LeafNode("code", text_node.text),
          TextType.LINK: lambda: LeafNode("a", text_node.text, {"href": text_node.url}),
          TextType.IMAGE: lambda: LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}),
        }

        return Text_Type_Node_HTML[text_node.text_type]()

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
      print(f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("All parent nodes must have children.")
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"