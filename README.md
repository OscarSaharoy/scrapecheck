# scrapecheck

I made this project because I had this problem after scraping text from the internet: given some text that the scraper returns, how can you check if it successfully got the page content or got stopped eg. by a challenge or paywall?

This uses a few regexes to build features from the text that is returned, and then does logistic regression or runs a random forest classifier on those features. It's not perfect but can give a good indication of whether the scraping worked, and the text evaluation is lightweight enough to run quickly on the client side too, rather than feeding the text through an LLM or something.
