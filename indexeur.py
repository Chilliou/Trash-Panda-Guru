from database import Database
from crawler import Crawler
import json
from tqdm import tqdm

class Site:
    def __init__(self, url, title, h1, meta, text):
        self.url = url
        self.title = title
        self.h1 = h1
        self.meta = meta
        self.text = " ".join(text)  # Convertissez le tuple en chaîne de caractères

class SiteMots:
    def __init__(self, siteUrl, mot, nbOccu, tf, idf=  None):
        self.site_url  = siteUrl
        self.mot = mot
        self.nbOccurence  = nbOccu
        self.tf = tf
        self.idf = idf

def get_nb_page_mot(mot):
    nb_idf = sum(1 for site in lst_Site_mot if site.mot == mot)
    idf_total[mot] = nb_idf


bdd = Database()
print("---------------- CREATION SITE ------------ ")
lst_Site = []
lst_site_sql = bdd.get_all_sites()
for row in lst_site_sql:
    url, json_data = row
    data = json.loads(json_data)
    site = Crawler(url, data["title"], data["h1"], data["meta"], data["text"])
    lst_Site.append(site)

print("---------------- RELATION SITE MOT ------------ ")
lst_Site_mot = []
lst_mot_sql = bdd.get_all_mots() 
i = 0
for mot in tqdm (lst_mot_sql):
    #print("---------------- MOT : ",i," ------------ ")
    i=i+1
    for site in lst_Site:
        if site.text.count(mot) > 0:
            nbOccu = site.text.count(mot)
            lst_Site_mot.append(SiteMots(site.url, mot, nbOccu, nbOccu/len(site.text.split())))

print("---------------- CALCUL DU IDF ------------ ")
idf_total = {}
for mot in tqdm(lst_mot_sql):
    get_nb_page_mot(mot)


nbPage = len(lst_Site)
print("-------- NB total mot site : ",len(lst_Site_mot),"---------")
for sitemot in tqdm(lst_Site_mot):
    sitemot.idf = nbPage/idf_total[sitemot.mot]


print("---------------- INSERT BASE ------------ ")
for sitemot in tqdm(lst_Site_mot):
    bdd.insert_mot_site(sitemot)
