import re
import requests
import logging
from bs4 import BeautifulSoup

URL_NAME_REGEX = r'\/([^\/]+)$'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
      {"tag": "table", "class": "infobox"},
      {"tag": "table", "class": "sidebar"},
      {"tag": "div", "class": "navbar"},
    ]
    for obj in objs_to_remove:
      for e in soup.find_all(obj["tag"], class_=obj["class"]):
        e.decompose()

    # Get the main page
    main_page = (
      soup
      .select_one("#mw-content-text")
      .find_all(elements_to_check)
    )

    first_link = None
    for p in main_page:
      # Remove italized text
      for e in p.find_all("i"):
        _ = e.decompose()

      # Get links in order
      for a in p.find_all("a", href=True):
        a_class = a.get("class")
        a_href = a.get("href")

        # Internal links don't have a class or are mw-redirect
        if not a_class or "mw-redirect" in a_class:
          # Check if citation
          if a_href.startswith("#cite"):
            continue
          
          # Check if parenthesized
          parenthesis_regex = fr'\([^\)]*{a}[^\)]*\)'
          if re.search(parenthesis_regex,str(p)):
            continue

          first_link = "https://en.wikipedia.org" + a_href
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
