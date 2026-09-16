# Website to CSV Scraper

Collects data from a website and saves it as a clean CSV file.

## What it collects:

|  Column   |                               Example                           |
|-----------|-----------------------------------------------------------------|
|  Title    | EU chief opens door for Canada to become 'associate member'     |
| Author    | hackernj                                                        |
| Points    | 175                                                             |
| Comments  | 110                                                             |
| URL       | https://www.bbc.com/news/articles/cjwyzrr9d3dko                 |


# Output -

90 records from 3 pages (30 per pages)
Sample output inlcluded: ''stories.csv'


## Notes for the cllient

- Records with missing data are logged, not silently dropped.
- Runs with a delay between pages to avoid overloading the site.
- Exports to CSV, opens directly in Excel.


# # How to run:

1. Open cmd and run the command 'pip install selenium'
2. run 'python hacker-news-scraper.py'
