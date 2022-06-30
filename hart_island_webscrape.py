# Webscraping from Hart Island website:

import requests
from bs4 import BeautifulSoup

URL = "https://www.hartisland.net/burial_records/search"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="content")

dead_elements = results.find_all("div", class_="columns large-9 edit-inner")

for dead_element in dead_elements:
    firstname_element = dead_element.find("td", class_="col-3")
    plot_element = dead_element.find("td", class_="col-5")
    deathdate_element = dead_element.find("td", class_="col-7 col-1")
    print(firstname_element.text.strip())
    print(plot_element.text.strip())
    print(deathdate_element.text.strip())
    print()