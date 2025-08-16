# scrapecheck

I made this project because I had this problem after scraping text from the internet: given some text that the scraper returns, how can you check if it successfully got the page content or got stopped eg. by a challenge or paywall?

This uses a few regexes to build features from the text that is returned, and then does logistic regression or runs a random forest classifier on those features. It's not perfect but can give a good indication of whether the scraping worked, and the text evaluation is lightweight enough to run quickly on the client side too, rather than feeding the text through an LLM or something.

## running the model

1. make sure python is installed, as well as all requirements - `pip install scikit-learn numpy`

2. run `./train.py` - this will save the model weights into `model.pkl`
```
(.pyenv) [oscarsaharoy@LCCC-MB-pTIY21 ~/projects/scrapecheck] $ ./train.py
fitting model
fitted model
(.pyenv) [oscarsaharoy@LCCC-MB-pTIY21 ~/projects/scrapecheck] $ ls
__pycache__     chars.txt       data            infer.py        model.pkl       README.md       train.py
```

3. pipe text into `./infer.py` - you can see here, nice article text gives a score around 0.84, and non-article UI text gives around 0.14.

```bash
(.pyenv) [oscarsaharoy@LCCC-MB-pTIY21 ~/projects/scrapecheck] $ echo "
Kitty Marion (1871–1944) was an activist who advocated for women's suffrage and birth control. Born in Germany, she immigrated to England in 1886 when she was 15 years old. She sang in music halls throughout Britain and became known in the industry for bringing attention to the sexism and sexual assaults that were common in the business. Marion was a prominent member of the British suffrage movement. She began her advocacy by selling copies of the newspaper Votes for Women, then progressed to militant protests, including riots, bombing and arson attacks; she was imprisoned several times for arson and bombing. On the outbreak of World War I, she left Britain for the United States. She joined the American birth control movement, and spent 13 years campaigning on street corners, selling the magazine Birth Control Review. Marion was arrested several times for distributing birth control information in violation of anti-obscenity laws. She died in New York in 1944.
" | ./infer.py
0.8409240057216918

(.pyenv) [oscarsaharoy@LCCC-MB-pTIY21 ~/projects/scrapecheck] $ echo "
Wikipedia's sister projects

Wikipedia is written by volunteer editors and hosted by the Wikimedia Foundation, a non-profit organization that also hosts a range of other volunteer projects:

    Commons logo
    Commons
    Free media repository
    MediaWiki logo
    MediaWiki
    Wiki software development
    Meta-Wiki logo
    Meta-Wiki
    Wikimedia project coordination
    Wikibooks logo
    Wikibooks
    Free textbooks and manuals
    Wikidata logo
    Wikidata
    Free knowledge base
    Wikinews logo
    Wikinews
    Free-content news
    Wikiquote logo
    Wikiquote
    Collection of quotations
    Wikisource logo
    Wikisource
    Free-content library
    Wikispecies logo
    Wikispecies
    Directory of species
    Wikiversity logo
    Wikiversity
    Free learning tools
    Wikivoyage logo
    Wikivoyage
    Free travel guide
    Wiktionary logo
    Wiktionary
    Dictionary and thesaurus

Wikipedia languages

This Wikipedia is written in English. Many other Wikipedias are available; some of the This Wikipedia is writow.
" | ./infer.py
0.1388240333655636
```
