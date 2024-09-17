# Wiki Web

This repo is designed to scrape random wikipedia pages,
click the first valid Wikipedia link,
on that page click the first valid link again,
and continue until it gets to a page it's already visited.
Why you ask?
Most pages will eventually get to the Philosphy Wikipedia article
(see [here](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy))
or get into a loop.
I wanted to pull my own data on this to analysis it.

## Running
1. On the first time, install any packages you may need: `pip install -r requirements.txt`
1. On the command line run `python wiki_web/main.py` to create one seed URL and see where it goes
1. For more options run `python wiki_web/main.py --help`
1. This will create three files:
  1. `debug.log` which will give you the debug logs for the run
  1. `seed.txt` a list of seed URLs
  1. `wiki_web.tsv` a tab-separated list of parent-child relationships for all the pages encountered

## How it works
1. Add random Wikipedia pages as seeds (or supply your own) (`wikiWeb.add_seeds()` or `wikiWeb.add_urls()`)
1. This adds urls to `wikiWeb.seeds` (`list`) and `wikiWeb.first_links` (a `dict` with all items initialized to `None`)
1. `wikiWeb.build_web()` iterates across all seeds
  1. 

## Initial analysis

## Future plans
- Create an interative display for the Wiki Web.
- Fix any bugs as they arise
