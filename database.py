import mysql.connector
from crawler import Site
import json
import requests

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="toor",
            database="google",
            port=4448
        )
        self.waiting_list = []

    def insert_data(self):
        count = 0
        if self.waiting_list:
            url = self.waiting_list.pop(0)
            if url not in Site.PROCESSED_URLS:
                site = Site(url)
                if site.crawl():
                    cursor = self.connection.cursor()
                    cursor.execute("INSERT INTO Site (SiteURL, SiteTitre, SiteJSON) VALUES (%s, %s, %s)", (site.url, site.title, json.dumps(site.to_json())))
                    self.waiting_list.extend(site.all_urls)
                    self.connection.commit()
                    cursor.close()
                    count += 1
        else:
            print("Waiting list is empty.")
        return count
    
    def get_all_sites(self):
        sites = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT SiteURL, SiteTitre, SiteJSON FROM Site")
        for row in cursor:
            url, title, json_data = row
            data = json.loads(json_data)
            site = Site(url, data["title"], data["h1"], data["meta"], data["text"])
            sites.append(site)
        cursor.close()
        return sites

dt = Database()
dt.waiting_list.append("https://fr.wikipedia.org/wiki/Singe")
total_iterations = 0
for _ in range(1000):
    count = dt.insert_data()
    total_iterations += count
    print(f"Iteration {_+1}: {count} sites added.")
print(f"Total iterations: {total_iterations}")