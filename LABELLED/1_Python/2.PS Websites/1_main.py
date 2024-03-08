from function import open_browser, get_links, get_list_items
import csv
from domainextraction import getDomain
import json

action = input('A. Start from scratch or B. Continue previous procedure')

URL = 'https://mediabiasfactcheck.com/conspiracy/'
open_browser(URL)

if action.lower() == 'a':
    list_items = get_list_items()
    try:
        csvfile = open('../../domains/sublists/mbfc_link_list.csv', 'a', newline='')
    except:
        csvfile = open('../../domains/sublists/mbfc_link_list.csv', 'w+', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=['domain', 'source', 'conspiracy level', 'pseudo-science level', 'factual reporting level', 'timestamp'])
    writer.writeheader()

if action.lower() == 'b':
    with open('new_tabs_list.json', 'r') as data:
        list_items = json.load(data)
    csvfile = open('../../domains/sublists/mbfc_link_list.csv', 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=['domain', 'source', 'conspiracy level', 'pseudo-science level', 'factual reporting level', 'timestamp'])

get_links(list_items, writer)
