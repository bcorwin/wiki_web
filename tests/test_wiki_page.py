import pytest
from bs4 import BeautifulSoup

import wiki_web.wiki_page as wp


@pytest.mark.parametrize(
    "tag,class_name,expected",
    {
        ("i", None, ' <div>div</div> <div class="a_class">div with class</div>'),
        ("div", None, '<i>italics</i>  <div class="a_class">div with class</div>'),
        ("div", "a_class", "<i>italics</i> <div>div</div> "),
    },
)
def test_remove_elements(tag: str, class_name: str, expected: str):
    base_text = (
        '<i>italics</i> <div>div</div> <div class="a_class">div with class</div>'
    )

    soup = BeautifulSoup(base_text, "html.parser")
    _ = wp.remove_elements(soup, tag, class_name)

    assert str(soup) == expected


@pytest.mark.parametrize(
    "inner_text,outer_text,expected",
    {
        (
            '<a href="/wiki/Help:IPA/Norwegian">[ˈʊ̂ʂlʊˌfjuːɳ]</a>',
            'The <b>Oslofjord</b> (<a href="/wiki/Help:IPA/Norwegian">[ˈʊ̂ʂlʊˌfjuːɳ]</a>)',
            True,
        ),
        (
            "<b>yes</b>",
            "<p>In parenthesis? (<b>yes</b>) <i>no</i></p>",
            True,
        ),
        ("<i>no</i>", "In parenthesis? (<b>yes</b>) <i>no</i>", False),
    },
)
def test_is_in_parenthesis(inner_text, outer_text, expected):
    outer_text = "<p>" + outer_text + "</p>"
    outer_element = BeautifulSoup(outer_text, "html.parser").find("p")
    inner_element = BeautifulSoup(inner_text, "html.parser").find()
    assert wp.is_in_parenthesis(inner_element, outer_element) is expected


@pytest.mark.parametrize(
    "text,expected",
    {
        ('<a href="/wiki/link">text</a>', True),
        ('<a href="/wiki/link" class="mw-redirect">text</a>', True),
        ('<a href="#cite_note-1" class="mw-redirect">text</a>', False),
        ('<a href="#cite_note-1">text</a>', False),
        ('<a href="/wiki/link" class="external text">text</a>', False),
    },
)
def test_is_valid_link(text, expected):
    element = BeautifulSoup(text, "html.parser").find("a")
    assert wp.is_valid_link(element) is expected
