# TODO: Add logging
# TODO: follow first link until it gets to philosophy, loops, or stops
import os
import csv
import requests
import logging

from wiki_page import wikiPage

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

logger = logging.getLogger("__main__." + __name__)


def random_wiki_page():
    res = requests.get(RANDOM_URL)
    return res.url


class wikiWeb:
    def __init__(self):
        logger.info("Wiki Web initialized.")
        self.first_links = {}

    def _add_page(self, page: wikiPage):
        first_link = wikiPage(page.get_first_link())
        self.first_links[page] = first_link
        if first_link not in self.first_links:
            self._add_page(first_link)
        else:
            logger.info(f"Stopping at {first_link}")

    def add_urls(self, urls: list | str):
        if isinstance(urls, str):
            urls = [urls]
        logger.info(f"Adding {len(urls)} url(s).")
        for url in urls:
            seed = wikiPage(url)
            self.first_links[seed] = None

    def add_seeds(self, n: int = 100):
        logger.info(f"Adding {n} seed(s).")
        for _ in range(n):
            seed = wikiPage(url=random_wiki_page())
            self.first_links[seed] = None

    def build_web(self):
        logger.info("Building the web.")
        seeds = [key for key, item in self.first_links.items() if item is None]
        for seed in seeds:
            logger.info(f"Clicking through {seed}")
            self._add_page(seed)

    def load_web(self, file_name="wiki_web.tsv"):
        # Loads a previously saved web. Helpful for adding more samples
        if not os.path.exists(file_name):
            logger.warning(f"{file_name} does not exist and hasn't been loaded.")
            return None
        logger.info(f"Loading {file_name}.")
        with open(file_name, "r") as file:
            reader = csv.reader(file, delimiter="\t")
            n = 0
            for row in reader:
                self.first_links[row[0]] = row[1]
                n += 1
            logger.info(f"{n} urls added")

    def save_web(self, file_name="wiki_web.tsv"):
        # Save the web as a tab-delimited file
        logger.info("Saving results.")
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file, delimiter="\t")
            for key, value in self.first_links.items():
                writer.writerow([key, value])
