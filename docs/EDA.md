# Exploratory Data Analysis

- JSON data
- 3500 rows

Contains attributes:
- _id
- source
- title
- author
- url
- published_at
- last_modified_at
- crawled_at
- header_image
- short_description
- raw_content
- content


## `Content` in Raw Data -> Problems

Example article:
https://edition.cnn.com/2011/09/30/sport/golf/dunhill/index.html

The raw json data contains `raw_content` and `content`. The former is the raw HTML object present on the web page. The latter contains (1) headline (2) image alt text and (3) article text. (n.b. The naming is potentially misleading. Web parsing frameworks such as newspaper3k, BeautifulSoup typically refer to "content" as the extracted body text, and NOT all text on a page stripped of HTML tags.)

The raw content parsing into "content" is sub-optimal as is. It contains several problematic elements:
- includes non-body-text elements (e.g. headline, alt text)
    - e.g. "...nine-under 63 at KingsbarnsStory highlightsTommy Fleetwood..."
    - e.g. "...unraveled.Powered by Livefyre'"
- includes timestamps
    - e.g "...Dunhill LinksBy Updated 2019 GMT (0419 HKT) September 30, 2011 England\'s..."
- removes end-of-sentence whitespace in some cases (i.e. no space after final periods)
    - e.g. "...put him back to four-under.Donald, who is hoping to..."
- no sentence-final punctuation in some cases (i.e. )
    - e.g. "Links Championship in Scotland They are on 12-under..."

For the above reasons it is preferable to do the parsing of raw_content ourselves


## Parsing raw content

I explored using Newspaper3k (Python library) to extract the full text. This works fine when parsing a URL or parsing full body HTML, but the raw_content is only a portion of html. 

Instead I tried using BeautifulSoup to parse the html. This worked. But the raw content contains both (1) highlights and (2) body text. There are div and li classes that are distinctive for the sections of the html. I used these classes to pull out those elements and add them to the Article object separately


## NER content

NER could be done on the title, highlights, description and/or the body text (or all of those). I choose to focus only on the body text. 



