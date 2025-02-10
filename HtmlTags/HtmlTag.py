class HtmlTag:
    def __init__(self, tag, attributes=None, children=None, self_closing=False):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.self_closing = self_closing
    
    def addChild(self, child):
        self.children.append(child)
    
    def addAttribute(self, key, value):
        self.attributes[key] = value
    
    def render(self):
        attr_string = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        if self.self_closing:
            return f"<{self.tag} {attr_string}/>"
        children_string = "".join(child.render() if isinstance(child, HtmlTag) else child for child in self.children)
        return f"<{self.tag} {attr_string}>{children_string}</{self.tag}>"