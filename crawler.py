import re
import requests
from bs4 import BeautifulSoup
import threading
from database import Database
import queue


class Crawler:

    def __init__(self, url=None, title=None, h1=None, meta=None, text=None, list_url=None):
        self.url = url
        self.title = title
        self.h1 = h1
        self.meta = meta
        self.text = text
        self.all_urls = []
        self.list_url = list_url

    def _clean_text(self, text):
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text.strip()

    def crawl(self):
        if(len(self.list_url) < 10):
            self.list_url = bdd.get_file_url()
        
        self.url = self.list_url[0]
        self.list_url.pop(0)
        print("Je bosse sur ", self.url)

        try:
            response = requests.get(self.url, timeout=3)
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
            self.title = self._clean_text(soup.find('title').text) if soup.find('title') else ""
            self.h1 = self._clean_text(soup.find('h1').text) if soup.find('h1') else ""
            self.meta = self._clean_text(str(soup.find('meta'))) if soup.find('meta') else ""
            self.text = self._clean_text(soup.get_text())
            self.all_urls = [filtered_url for link in soup.find_all('a')
                 if (filtered_url := self._filter_url(link.get('href'))) is not None]
            bdd.insert_list_file_url(self.all_urls)
            bdd.validate_url(self.url)
            bdd.insert_site(self)
        except Exception as e:
            print(f"Error crawling {self.url}: {e}")
            bdd.validate_url(self.url)


    def _filter_url(self, url):
        if url and (url.startswith('http') or url.startswith('/')):
            # Charger la liste noire depuis un fichier
            with open('blocklist.txt', 'r') as f:
                blocklist = [line.strip() for line in f]
            
            # Vérifier si l'URL est dans la liste noire
            if any(domain in url for domain in blocklist):
                return None
            
            if url.startswith('/'):
                parsed_url = requests.utils.urlparse(self.url)
                return f"{parsed_url.scheme}://{parsed_url.netloc}{url}"
            else:
                parsed_url = requests.utils.urlparse(url)
                if parsed_url.netloc == requests.utils.urlparse(self.url).netloc:
                    return None  # Ignorer les liens internes au même domaine
                return url.strip()
        return None

    def to_json(self):
        return {
            "title": self.title,
            "h1": self.h1,
            "meta": self.meta,
            "text": self.text,
        }
    
    def __str__(self) -> str:
        return f"{self.url} - {self.title}"
    
""" 
bdd = Database();
list_url = bdd.get_file_url()

crawler = Crawler(list_url=list_url)
while True:
    crawler.crawl()
"""
