import logging

from wiki_web import wikiWeb

logging.basicConfig(
    level=logging.INFO,
    format="\t| ".join(
        "%(asctime)s",
        "%(levelname)s",
        "%(name)s.%(funcName)s.%(lineno)d",
        "%(message)s",
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

ww = wikiWeb()
# ww.load_web()
ww.add_seeds(10)
ww.build_web()
ww.save_web()
