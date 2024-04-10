#! bin/python3

"""
The program prepares the schema structure as of the Microsoft's Azure datastructure to download the data 
and create schema stucture
"""

import requests
import json
from bs4 import BeautifulSoup

url = "https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/tables-resourcetype"

page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")
tables = []

for li in soup.find_all('li'):
    a = li.find_all("a")
    if len(a)>0:
        if a[0].get("data-linktype", None) == 'relative-path':
            if a[0]['href'] not in tables:
                tables.append(a[0]['href'])

tables = list(set(tables))

baseurl = 'https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/'

db_schemas = []

try:
    with open('db.schemas.json') as f:
        db_schemas = json.load(f)
        if db_schemas is None:
            db_schemas = []
except FileNotFoundError:
    db_schemas = []

db_schema = {
    "db_id": "azure_log_space",
    "table_names_original": [],
    "table_names": [],
    "column_names_original": [],
    "column_types": [],
    "column_description": [],
    "column_names": [],
    "primary_keys": [],
    "foreign_keys": []
}

baseurl = "https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/"

index = 0

for table in tables:
    print("generating for table", table)
    db_schema["table_names_original"].append(table)
    db_schema["table_names"].append(table)
    url = baseurl+ table
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for el in soup.find_all("table")[1].find_all("tr"):
        tds = el.find_all("td")
        if len(tds)>0:
            db_schema["column_names_original"].append([index,tds[0].text])
            db_schema["column_names"].append([index,tds[0].text])
            db_schema["column_description"].append([index,tds[2].text])
            db_schema["column_types"].append(tds[1].text)
    index+=1
db_schemas.append(db_schema)


with open("db_schema.json","w") as outfile:
    json.dump(db_schemas,outfile, indent=4)
