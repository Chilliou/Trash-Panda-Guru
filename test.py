from database import Database

db = Database()
sites = db.get_all_sites()

#for site in sites:
#    print(f"URL: {site.url}")
#    print(f"Title: {site.title}")
#    print(f"H1: {site.h1}")
#    print(f"Meta: {site.meta}")
#    print(f"Text: {site.text}")
#    print("---")


for site in sites:
    print(f"URL: {site.url}")
    print(f"Title: {site.title}")
    print(f"Occurence de dragon: {site.text.count('dragon')}")
