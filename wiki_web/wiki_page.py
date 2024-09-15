import re
import requests
import logging
from bs4 import BeautifulSoup, element

URL_NAME_REGEX = r'\/([^\/]+)$'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def remove_elements(soup: BeautifulSoup, tag:str, class_name:str = None):
  ### Remove elements based on tag and class (optional)
  for e in soup.find_all(tag, class_ = class_name):
    e.decompose()

def is_in_parenthesis(sub_element: element.Tag, element:element.Tag):
  ### Check if sub_element is surrounded by parenthesis in elementn text
  parenthesis_regex = fr'\([^\)]*{sub_element}[^\)]*\)'
  return re.search(parenthesis_regex, str(element)) is not None

def is_valid_link(element: element.Tag):
  ### Checks if the link is valid per the getting to philosphy rules
  classes = element.get("class", [])
  href = element.get("href")

  # Internal links don't have a class or are mw-redirect
  if href.startswith("#cite"):
    return False
  if len(classes) == 0 or "mw-redirect" in classes:
    return True
  return False

class wikiPage():
  def __init__(self, url: str):
    self.url = url
    self.name = re.search(URL_NAME_REGEX, url).group(1)
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
    return not(self == other)

  def _get_first_link(self, html_content):
    # TODO: break this into helper functions and test them
    elements_to_check = ["p", "ol", "ul"]
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove various elements
    objs_to_remove = [
      {"tag": "i"},
      {"tag": "div", "class_name": "navbar"},
      {"tag": "table", "class_name": "infobox"},
      {"tag": "table", "class_name": "sidebar"},
    ]
    for obj in objs_to_remove:
      remove_elements(soup, **obj)

    # Get the main page
    main_page = (
      soup
      .select_one("#mw-content-text")
      .find_all(elements_to_check)
    )

    first_link = None
    for p in main_page:
      # Check links in order
      for a in p.find_all("a", href=True):
        if is_valid_link(a) and not is_in_parenthesis(a, p):
          first_link = "https://en.wikipedia.org" + a.get("href")
          return first_link
    return "No valid link found."
      
  def get_first_link(self):
    # If I've already found this link, return it. Otherwise, find it.
    if not self._first_link:
      res = requests.get(self.url)
      if res.status_code != 200:
        first_link = res.reason
      else:
        logger.debug(res.url)
        first_link = self._get_first_link(res.content)

      self._first_link = first_link
    return self._first_link
