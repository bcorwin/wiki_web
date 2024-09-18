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
    - `debug.log` which will give you the debug logs for the run
    - `seed.txt` a list of seed URLs
    - `wiki_web.tsv` a tab-separated list of parent-child relationships for all the pages encountered

## How it works
1. Initialize: `ww = wikiWeb()`
1. (optional) `ww.load_web()` loads a previously run web
(this speeds up searching since the algorithm stops once it finds a link that's already been proceessed
and enables the user to run the process in batches)
1. Add random Wikipedia pages as seeds (`ww.add_seeds()`) and/or or supply your own (`ww.add_urls()`), this adds urls to:
    - `ww.seeds` a `list` of all seeds
    - `ww.first_links` a `dict` that maps a Wikipedia page to it's first valid link (initialized to `None` for all seeds)
1. `ww.build_web()` iterates across all seeds (i.e. links that have not yet been processed), for each seed it:
    1. Finds the first valid link (see next step)
    2. If that link is an error, break
    3. If that link has already been procssed, break
    4. Otherwise, find the first valid link of the new link
1. Finding the first valid link:
    1. Checks only a set
       [list]([url](https://github.com/bcorwin/wiki_web/blob/3ba17a04678d99dfd5f364f19541e4b2109c78a9/wiki_web/wiki_page.py#L97))
       of html elements (`p`, `ol` and `ul`)
    1. Removes a [list]([url](https://github.com/bcorwin/wiki_web/blob/3ba17a04678d99dfd5f364f19541e4b2109c78a9/wiki_web/wiki_page.py#L102))
        of `tag` / `class` combinations because they are things like navbars that appear, in code,
        before the first paragraph so we don't want to process them
    1. Loops through all the `a` tags and finds the first link that is internal, not in italics, and not in parenthesis. 

## Initial analysis
TODO: 
- philosophy loop size
- where enters the loop
- average clicks to philosophy
- percent that go to philo
- average loop length
- any other secondary ends?
- percent errors

## Future plans
- Create an interative display for the Wiki Web.
- Fix any bugs as they arise
