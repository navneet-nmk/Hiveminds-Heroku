import requests
from bs4 import BeautifulSoup
import csv


# Declaration of constants
MAX_SEQUENCE_LENGTH = 1000
MAX_NB_WORDS = 20000

url =  "https://api.nytimes.com/svc/search/v2/articlesearch.json"
api_key = "2ba396b683c14b46a152eb84639c6d3a"
q = "36 hours"
params = {"api-key": api_key,
    "q": q
}
response = requests.get(url, params=params)
json_data = response.json()
urls = []
# Parsing the json data
docs = json_data['response']['docs']
for d in docs:
    urls.append(d['web_url'])


def find_text(url):
    reviews = {}
    response = requests.get(url)
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    title = parser.find("head").title.text
    names = parser.find_all("div", class_="listy_body")
    for n in names[1:]:
        heads = n.find_all("h3")
        paras = n.find_all("p")
        for h, ps in zip(heads, paras):
            h = h.text.split(") ")[1]
            r = ps.text
            reviews[h] = r
    return reviews, title


for u in urls:
    reviews, title = find_text(u)
    with open(title + ".csv", "w") as file:
        w = csv.writer(file)
        w.writerows(reviews.items())

print("Created the files")


