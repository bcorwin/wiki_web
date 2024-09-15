# TODO: add pre-commit hooks
import logging

from wiki_web import wikiWeb

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s\t| %(levelname)s\t| %(name)s.%(funcName)s.%(lineno)d\t| %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

ww = wikiWeb()
ww.load_web()
ww.add_seeds(100)
ww.build_web()
ww.save_web()