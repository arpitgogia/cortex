import newspaper
import time
import datetime
import nltk
from urllib.parse import urlparse
from .models import AllUrl, Article, ArticleStates


class ContentExtractor:

    def __init__(self):
        nltk.download('punkt')

    def extract_content(self):
        urls = AllUrl.objects.all()
        for entry in urls:
            entry_html = entry.html
            entry_url = entry.url
            article = self.extract_content_wrapper(entry_html, entry_url)
            article.save()

    def extract_content_wrapper(self, html, url):
        start = time.time()
        print(html)
        article = newspaper.Article(url='')
        article.download(html=html)
        article.parse()
        article.nlp()

        article2 = Article()
        try:
            article2.url = url
            article2.title = article.title
            article2.domain_name = urlparse(url).hostname
            article2.text = article.text
            article2.keywords = str(article.keywords)
            article2.authors = str(article.authors)
            article2.tags = list(article.tags)
            article2.summary = article.summary
            # article2.links
            end = time.time()
            article2.parse_time = end - start
            article2.state = ArticleStates.EXTRACTED.value
            # article2.html = article.html
            # ISO Format is the standard of maintaining datetime
            article2.publish_date = article.publish_date.isoformat()
        except:
            now = datetime.datetime.now().isoformat()
            article2.publish_date = now[:now.index('T')]
            print('Some fields may be missing')
        return article2
