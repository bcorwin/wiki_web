import logging

from wiki_web import wikiWeb

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("debug.log")
fh.setLevel(logging.DEBUG)
fh.addFilter(logging.Filter("__main__"))

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s\t| %(name)s.%(funcName)s\t| %(levelname)s\t| %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


ww = wikiWeb()
ww.load_web()
ww.add_seeds(1)
ww.build_web()
ww.save_web()
