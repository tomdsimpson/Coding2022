# Tom Simpson
# 24/08/22
# Scraping random wikipedia articles

import requests
import bs4


allowlist = ['p','a','b']
url = "https://en.wikipedia.org/wiki/Special:Random"
page = requests.get(url)
html = page.text

soup = bs4.BeautifulSoup(html, features="lxml")
title = soup.h1.text
text_elements = [t for t in soup.find_all(text=True) if t.parent.name in allowlist]

#print(title)
#print(text_elements)

new_text= ""
write = False

for x in text_elements:
    if x == title:
        write = True
    elif x == "edit":
        write = False
    elif x[0] == "[":
        pass
    elif write:
        new_text += x

print(title + new_text)