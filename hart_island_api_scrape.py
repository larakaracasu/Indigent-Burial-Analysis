import requests
import json
import pandas as pd
import datetime as dt
import csv

# To access data as JSON:

# response = requests.get("https://data.cityofnewyork.us/resource/f5mc-f3zp.json")

# def jprint(obj):
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

# jprint(response.json())

# To access data as DataFrame:

resp = requests.get('https://data.cityofnewyork.us/resource/f5mc-f3zp.json')
txt = resp.json()
data = pd.DataFrame(txt)
#print(data)

data.to_csv('hart_data.csv', encoding='utf-8', index=False)

hart_data_uncleaned = pd.read_csv("hart_data.csv")
hart_data_uncleaned['cleaned_death_date'] = hart_data_uncleaned['death_date'].str[:10]
hart_data_uncleaned = hart_data_uncleaned.drop('death_date', 1)
hart_data_uncleaned['cleaned_death_date'] = pd.to_datetime(hart_data_uncleaned.cleaned_death_date, errors = 'coerce')
hart_data_uncleaned['death_date'] = hart_data_uncleaned['cleaned_death_date'].dt.strftime('%m-%d-%Y')
hart_data_uncleaned = hart_data_uncleaned.drop('cleaned_death_date', 1)
#hart_data_uncleaned['death_date'] = hart_data_uncleaned['death_date'].str[:10]

for value in hart_data_uncleaned['age']:
    if isinstance(value, int):
        hart_data_uncleaned.age = hart_data_uncleaned.age.astype(int)

pd.options.display.float_format = '{:,.0f}'.format

hart_data_uncleaned.to_csv('hart_data_cleaned.csv', encoding='utf-8', index=False)
print(hart_data_uncleaned)