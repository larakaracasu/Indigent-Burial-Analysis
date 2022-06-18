#################################################################################
# SCRAPING FOR FRESNO LIBRARY INDIGENT BURIAL RECORDS, written by Lara Karacasu #
#################################################################################

# Note: After running 'pip install BeautifulSoup' and 'pip install requests,' one must save this file as UTF-8

# IMPORT LIBRARIES
from bs4 import BeautifulSoup
import requests
import pandas as pd

# PARSE PAGE
url = "https://www.fresnolibrary.org/heritage/cemetery/Potters_Field_web/index.html"
rawpage = requests.get(url).text
soup = BeautifulSoup(rawpage, 'html.parser')

# print(soup) 
# We see that the table is loaded inside an iFrame -> parse this URL inside
# We want the iFrame link to read 'https://www.fresnolibrary.org/heritage/cemetery/Potters_Field_web/potters%20A-B.htm'
# But there are 13 total links of this type (replacing A-B with C-D and so on), so we must scrape all of these links first

src_list = []
for link in soup.find_all('a', href=True):
    if '/potters' in str(link):
        src_list.append(link.text)
src_list = src_list[1:]
# print(src_list)
# 'A-B', 'C-D' and so on

iframe_src = soup.find("iframe").attrs["src"]
iframe_src = iframe_src.replace('../../', '') # remove "../../" from src

def scrape_table(src):

    # ALLOW ACCESS TO VARS
    global soup
    global url
    global iframe_src

    # OBTAIN IFRAME LINK
    iframe_src = iframe_src[:35] + src + iframe_src[38:42] # assemble individualized link to be scraped for each link ending
    print(iframe_src)
    url = url[:39] # replace URL with the desired URL stem
    iframe_link = url + iframe_src # concatenate URL fragments

    # PARSE IFRAME PAGE
    page = requests.get(iframe_link).text
    soup = BeautifulSoup(page, 'html.parser')

    # CREATE DF
    table_headings = soup.find_all("th")
    clean_headings = []
    for heading in table_headings:
        heading = str(heading)
        heading = heading.replace('<th>','').replace('</th>', '')
        clean_headings.append(heading)

    table = soup.find_all("table")[1] # using the first table on the iFrame
    df = pd.DataFrame(columns = clean_headings)
    for row in table.tbody.find_all('tr'):    
        columns = row.find_all('td')
        if (columns != []):
            name = columns[0].text
            age = columns[1].text
            sex = columns[2].text
            born = columns[3].text
            died = columns[4].text
            burieddied = columns[5].text
            tract = columns[6].text
            blocksection = columns[7].text
            lotrow = columns[8].text
            grave = columns[9].text
            mortuary = columns[10].text
            misc = columns[11].text
            df = df.append({'Name': name,  'Age': age, 'Sex': sex, 'Born': born, 'Died': died, 'Buried/Died': burieddied, 'Tract': tract, 'Block/Section': blocksection, 'Lot/Row': lotrow, 'Grave#': grave, 'Mortuary': mortuary, 'Misc Info': misc}, ignore_index=True)
    return(df)

for src in src_list:
    df = scrape_table(src)
    print(df)
    df.to_csv('fresno-' + src + '.csv')