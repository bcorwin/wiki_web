import re
import requests
import logging
from bs4 import BeautifulSoup, element

URL_NAME_REGEX = r"\/([^\/]+)$"

logger = logging.getLogger("__main__." + __name__)


def remove_elements(soup: BeautifulSoup, tag: str, class_name: str = None):
    # Remove elements based on tag and class (optional)
    for e in soup.find_all(tag, class_=class_name):
        e.decompose()


def match_parentheses(text: str):
    if not re.search(r"[\(\)]", text):
        return text
    bracket_stack = []
    brackets_numbered = []
    count = 0
    for char in text:
        if char == "(":
            count += 1
            bracket_stack.append(("(", count))
            brackets_numbered.append(("(", count))
        elif char == ")":
            if len(bracket_stack) == 0:
                raise Exception("Unmatched closed parentheses.")
            else:
                _, bracket_num = bracket_stack.pop()
                brackets_numbered.append((")", bracket_num))
    if len(bracket_stack):
        raise Exception("Unmatched open parentheses.")

    text_split = re.split(r"[\(\)]", text)
    output = ""
    for s in text_split:
        if len(brackets_numbered):
            bracket, num = brackets_numbered.pop(0)
            output += s + f"{bracket}<{num}>"
    return output


def is_in_parenthesis(sub_element: element.Tag, element: element.Tag):
    # Check if sub_element is surrounded by parenthesis in elementn text
    # parenthesis_regex = rf"\([^\)]*{re.escape(str(sub_element))}[^\)]*\)"
    # html_search = re.search(parenthesis_regex, str(element)) is not None

    # The above fails when there (something (like) this)
    sub_text = match_parentheses(sub_element.get_text())
    outer_text = match_parentheses(element.get_text())
    matched_parenthesis_regex = rf"\(<(\d+)>.*{re.escape(sub_text)}.*\)<\1>"
    text_search = re.search(matched_parenthesis_regex, outer_text) is not None

    return text_search


def is_valid_link(element: element.Tag):
    # Checks if the link is valid per the getting to philosphy rules
    classes = element.get("class", [])
    href = element.get("href")

    # Internal links don't have a class or are mw-redirect
    if href.startswith("#cite"):
        return False
    if len(classes) == 0 or "mw-redirect" in classes:
        return True
    return False


class wikiPage:
    def __init__(self, url: str):
        self.url = url
        name = re.search(URL_NAME_REGEX, url)
        self.name = name.group(1) if name else url
        self._first_link = None

    def __str__(self):
        return self.url

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not (self == other)

    def _get_first_link(self, html_content):
        elements_to_check = ["p", "ol", "ul"]
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove various elements
        objs_to_remove = [
            {"tag": "i"},
            {"tag": "div", "class_name": "navbar"},
            {"tag": "div", "class_name": "hidden-content"},
            {"tag": "table", "class_name": "infobox"},
            {"tag": "table", "class_name": "sidebar"},
            {"tag": "a", "class_name": "oo-ui-buttonElement-button"},
            {"tag": "sup", "class_name": "ext-phonos-attribution"},
        ]
        for obj in objs_to_remove:
            remove_elements(soup, **obj)

        # Get the main page
        main_page = soup.select_one("#mw-content-text").find_all(elements_to_check)

        first_link = None
        for p in main_page:
            # Check links in order
            for a in p.find_all("a", href=True):
                if is_valid_link(a) and not is_in_parenthesis(a, p):
                    first_link = "https://en.wikipedia.org" + a.get("href")
                    return first_link
        raise Exception("No valid link found.")

    def get_first_link(self):
        # If I've already found this link, return it. Otherwise, find it.
        if not self._first_link:
            res = requests.get(self.url)
            if res.status_code != 200:
                logger.warning(res.reason)
                first_link = "ERROR: " + res.reason
            else:
                logger.debug(res.url)
                try:
                    first_link = self._get_first_link(res.content)
                except Exception as e:
                    logger.warning(str(e))
                    first_link = "ERROR: " + str(e)

            self._first_link = first_link
        return self._first_link
