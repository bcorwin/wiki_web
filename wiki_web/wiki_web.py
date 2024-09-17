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
        self.seeds = []

    def _add_page(self, page: wikiPage):
        url = page.get_first_link()
        first_link = wikiPage(url)
        self.first_links[page] = first_link
        if url.startswith("ERROR"):
            pass
        elif first_link not in self.first_links:
            self._add_page(first_link)
        else:
            logger.debug(f"Stopping at {first_link}")

    def add_urls(self, urls: list | str):
        if isinstance(urls, str):
            urls = [urls]
        logger.info(f"Adding {len(urls)} url(s).")
        for url in urls:
            seed = wikiPage(url)
            self.first_links[seed] = None
            self.seeds.append(seed)

    def add_seeds(self, n: int = 100):
        logger.info(f"Adding {n} seed(s).")
        for _ in range(n):
            seed = wikiPage(url=random_wiki_page())
            self.first_links[seed] = None
            self.seeds.append(seed)

    def build_web(self):
        logger.info("Building the web.")
        seeds = [key for key, item in self.first_links.items() if item is None]
        n = 1
        for seed in seeds:
            logger.info(f"[{n:3}] Clicking through {seed}")
            self._add_page(seed)
            n += 1

    def load_web(self, file_name="outputs/wiki_web.tsv"):
        # Loads a previously saved web. Helpful for adding more samples
        if not os.path.exists(file_name):
            logger.warning(f"{file_name} does not exist and hasn't been loaded.")
            return None
        logger.info(f"Loading {file_name}.")
        with open(file_name, "r") as file:
            reader = csv.reader(file, delimiter="\t")
            n = 0
            for row in reader:
                parent = wikiPage(url=row[0])
                child = wikiPage(url=row[1])
                self.first_links[parent] = child
                n += 1
            logger.info(f"{n} urls added")

    def save_web(self, file_name="outputs/wiki_web.tsv"):
        # Save the web as a tab-delimited file
        logger.info("Saving results.")
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file, delimiter="\t")
            for key, value in self.first_links.items():
                writer.writerow([key, value])
        self.save_seeds()

    def save_seeds(self, file_name="outputs/seeds.txt"):
        # Save the seeds as a text file
        logger.info("Saving seeds.")
        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file, delimiter="\t")
            for seed in self.seeds:
                writer.writerow([seed])
