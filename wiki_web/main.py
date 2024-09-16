import click
import logging

from wiki_web import wikiWeb

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("outputs/debug.log")
fh.setLevel(logging.DEBUG)
fh.addFilter(logging.Filter("__main__"))

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(name)s.%(funcName)s | %(levelname)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


@click.command()
@click.option("-s", "--seeds", default=1, help="Number of seeds to add.")
@click.option("--load/--no-load", default=True, help="Load the previous output files")
@click.option(
    "--load-file-name", default="outputs/wiki_web.tsv", help="Output file name to load."
)
@click.option(
    "--save-file-name", default="outputs/wiki_web.tsv", help="File to save to."
)
def main(seeds, load, load_file_name, save_file_name):
    ww = wikiWeb()
    if load:
        ww.load_web(file_name=load_file_name)
    ww.add_seeds(seeds)
    ww.build_web()
    ww.save_web(file_name=save_file_name)


main()
