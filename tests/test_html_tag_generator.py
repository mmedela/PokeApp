import pytest

from HtmlTags.HtmlTag import HtmlTag

def testCreateHtmlTag():
    tag = HtmlTag("div")
    assert tag.tag == "div"
    assert tag.attributes == {}
    assert tag.children == []
    assert not tag.self_closing


def testCreateHtmlTagWithAttributes():
    tag = HtmlTag("a", attributes={"href": "https://example.com"})
    assert tag.tag == "a"
    assert tag.attributes == {"href": "https://example.com"}
    assert tag.children == []
    assert not tag.self_closing


def testCreateSelfClosingTag():
    tag = HtmlTag("img", self_closing=True, attributes={"src": "image.jpg", "alt": "Image"})
    assert tag.tag == "img"
    assert tag.attributes == {"src": "image.jpg", "alt": "Image"}
    assert tag.children == []
    assert tag.self_closing is True
    rendered = tag.render()
    assert rendered == '<img src="image.jpg" alt="Image"/>'


def testAddChild():
    parent = HtmlTag("div")
    child = HtmlTag("p")
    parent.addChild(child)
    assert len(parent.children) == 1
    assert parent.children[0] == child


def testAddAttribute():
    tag = HtmlTag("a")
    tag.addAttribute("href", "https://example.com")
    assert tag.attributes == {"href": "https://example.com"}


def test_render_with_children():
    parent = HtmlTag("div")
    child = HtmlTag("p", children=["Hello, World!"])
    parent.addChild(child)
    rendered = parent.render()
    expected_render = '<div ><p >Hello, World!</p></div>'
    assert rendered == expected_render


def test_render_self_closing_tag():
    tag = HtmlTag("img", self_closing=True, attributes={"src": "image.jpg", "alt": "Image"})
    rendered = tag.render()
    expected_render = '<img src="image.jpg" alt="Image"/>'
    assert rendered == expected_render


def test_render_tag_with_multiple_attributes_and_children():
    tag = HtmlTag("div", attributes={"class": "container", "id": "main"})
    child1 = HtmlTag("p", children=["First paragraph"])
    child2 = HtmlTag("p", children=["Second paragraph"])
    tag.addChild(child1)
    tag.addChild(child2)
    rendered = tag.render()
    expected_render = '<div class="container" id="main"><p >First paragraph</p><p >Second paragraph</p></div>'
    assert rendered == expected_render
