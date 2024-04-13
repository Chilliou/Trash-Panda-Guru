import mysql.connector
import json
import requests

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="toor",
            database="gogoRaccoon",
            port=4448
        )
    """""
    def insert_data(self):
        count = 0
        if self.waiting_list:
            url = self.waiting_list.pop(0)
            site = Crawler(url)
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
            site = Crawler(url, data["title"], data["h1"], data["meta"], data["text"])
            sites.append(site)
        cursor.close()
        return sites
    """

    def insert_site(self, site):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE INTO Site (siteUrl,siteJSON) VALUES (%s, %s)"
        val = (site.url, json.dumps(site.to_json()))
        print("voici ",site.url)
        cursor.execute(query, val)
        self.connection.commit()
        cursor.close()
    
    def get_file_url(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT url FROM FileUrl WHERE fileTraite = False limit 100")
        result = cursor.fetchall()
        cursor.close()
        urls = []
        for row in result:
            if isinstance(row[0], str):
                urls.append(row[0])

        return urls
    
    def validate_url(self, url):
        cursor = self.connection.cursor()
        query="UPDATE FileUrl SET fileTraite = True WHERE url = %s"
        cursor.execute(query, (url,))
        self.connection.commit()
        cursor.close()

    
    def insert_list_file_url(self, list_url):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE INTO FileUrl (url) VALUES (%s)"
        cursor.executemany(query, [(url,) for url in list_url])
        self.connection.commit()
        cursor.close()


"""
dt = Database()
total_iterations = 0
for _ in range(1000):
    count = dt.insert_data()
    total_iterations += count
    print(f"Iteration {_+1}: {count} sites added.")
print(f"Total iterations: {total_iterations}")
"""