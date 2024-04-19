import mysql.connector
import json
import requests

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YourRootPassword",
            database="gogoRaccoon",
            port=4448
        )

    def insert_mot_site(self, siteMot):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE INTO SiteMots (siteID, motID, nbOccurence, tf, idf) VALUES (%s, %s, %s, %s, %s)"
        val = (self.get_site_id(siteMot.site_url), self.get_mot_id(siteMot.mot), siteMot.nbOccurence, siteMot.tf, siteMot.idf)
        cursor.execute(query, val)
        cursor.close()  # Close the cursor
        self.connection.commit()
       

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results

    def get_mot_id(self, mot):
        query = "SELECT motID FROM Mots WHERE mot=%s"
        results = self.execute_query(query, (mot,))
        if results:
            return results[0][0]  # Return the first element of the first tuple
        else:
            return None

    def get_site_id(self, site_url):
        query = "SELECT SiteID FROM Site WHERE siteUrl=%s"
        results = self.execute_query(query, (site_url,))
        if results:
            return results[0][0]  # Return the first element of the first tuple
        else:
            return None


    def get_all_sites(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT SiteURL, SiteJSON FROM Site")
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_all_mots(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT mot FROM Mots")
        result = cursor.fetchall()
        cursor.close()    
        mots = []
        for row in result:
            if isinstance(row[0], str):
                mots.append(row[0])

        return mots

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

