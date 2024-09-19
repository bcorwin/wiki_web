# Wiki Web

This repo is designed to scrape random wikipedia pages,
click the first valid Wikipedia link,
on that page click the first valid link again,
and continue until it gets to a page it's already visited.
Why you ask?
Most pages will eventually get to the Philosophy Wikipedia article
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
(this speeds up searching since the algorithm stops once it finds a link that's already been processed
and enables the user to run the process in batches)
1. Add random Wikipedia pages as seeds (`ww.add_seeds()`) and/or or supply your own (`ww.add_urls()`), this adds urls to:
    - `ww.seeds` a `list` of all seeds
    - `ww.first_links` a `dict` that maps a Wikipedia page to it's first valid link (initialized to `None` for all seeds)
1. `ww.build_web()` iterates across all seeds (i.e. links that have not yet been processed), for each seed it:
    1. Finds the first valid link (see next step)
    2. If that link is an error, break
    3. If that link has already been processed, break
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
This [analysis](analysis\analysis.ipynb) is meant only to be a part I -
looking at high level numbers and a more detailed analysis will
come the [future](#future-plans).

I ran Wiki Web using 1K seeds
which resulted in about 2.4K additional pages and 3 distinct errors:
| Node type   |   Count |
|:------------|--------:|
| page        |    2413 |
| seed        |    1000 |
| error       |       3 |
| philosophy  |       1 |

### Errors
Only 7 seeds (0.7%) led to one of those three errors
(with an average number of clicks of 2.3).
I haven't yet dug into the 6 unmatched parentheses errors yet but, often,
they comes from human error
(e.g. a parentheses being dropped in writing or
one bracket being left in italics).
An error rate of 0.7% is very minimal so digging into this is low priority
but I want to look more into them for the next analysis.

### Getting to Philosophy
Of the 2K seeds, 43.9% led to Philosophy using an average of 13.4 clicks.

*Distribution of the number of clicks to get to Philosophy*
![Distribution of the number of clicks to get to Philosophy](image.png)

According to
[Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy),
a 2016 study showed that 97% of all articles led to Philosophy.
My results of 44% are way off from this,
so either things have changed,
or my algorithm is off.
I'll save this for the future analysis.

### How they arrive at Philosophy
If you start with Philosophy
you'll end up back there in 12 clicks.
This is called a *cycle*.

*The philosophy cycle:*
![The philosophy cycle](image-1.png)

Once a page leads to any of the pages in the cycle,
you'll end up getting to philosophy in no more than 11 clicks.
Which led me to wonder,
which entry point into the cycle was the most common.
Philosophy, perhaps unsurprisingly, was the most common entry point (73%)
for my 1K seeds. This was followed by Mathematics (7%) and Reason (6%).
| Entry to the Philosophy cycle             |   Number of seeds |   Average clicks to entry |   % of seeds |
|:------------------------------------------|------------------:|--------------------------:|-------------:|
| https://en.wikipedia.org/wiki/Philosophy  |               319 |                      13.6 |         72.7 |
| https://en.wikipedia.org/wiki/Mathematics |                31 |                       8.2 |          7.1 |
| https://en.wikipedia.org/wiki/Reason      |                26 |                       7.8 |          5.9 |
| https://en.wikipedia.org/wiki/Awareness   |                22 |                       7.5 |          5   |
| https://en.wikipedia.org/wiki/Reality     |                18 |                       5.4 |          4.1 |
| https://en.wikipedia.org/wiki/Existence   |                17 |                       8.4 |          3.9 |
| https://en.wikipedia.org/wiki/Geometry    |                 6 |                       7   |          1.4 |

## Future plans
- Why are my results so much different?
- Create an interactive display for the Wiki Web.
- Fix any bugs as they arise
- Look into other possible attractors
- Average cycle lengths
- Look into better handling unmatched parenthesis

