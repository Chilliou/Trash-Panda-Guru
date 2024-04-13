import re
import requests
from bs4 import BeautifulSoup

class Site:
    PROCESSED_URLS = set()

    def __init__(self, url, title=None, h1=None, meta=None, text=None):
        self.url = url
        self.title = title
        self.h1 = h1
        self.meta = meta
        self.text = text
        self.all_urls = []

    def _clean_text(self, text):
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text.strip()

    def crawl(self):
        if self.url in self.PROCESSED_URLS or self.url is None or not self.url.strip():
            return False
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = self._clean_text(soup.find('title').text) if soup.find('title') else ""
            h1 = self._clean_text(soup.find('h1').text) if soup.find('h1') else ""
            meta = self._clean_text(str(soup.find('meta'))) if soup.find('meta') else ""
            text = self._clean_text(soup.get_text())
            if title and h1 and meta and text:
                self.title = title
                self.h1 = h1
                self.meta = meta
                self.text = text
                self.all_urls = [self._filter_url(link.get('href')) for link in soup.find_all('a')]
                self.PROCESSED_URLS.add(self.url)
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error crawling {self.url}: {e}")
            return False

    def _filter_url(self, url):
        if url and (url.startswith('http') or url.startswith('/')):
            if url.startswith('/'):
                return self.url.rstrip('/') + url
            else:
                return url.strip()
        return None

    def to_json(self):
        return {
            "url": self.url,
            "title": self.title,
            "h1": self.h1,
            "meta": self.meta,
            "text": self.text,
        }