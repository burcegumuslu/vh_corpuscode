import json, os
from trafilatura import fetch_url, extract, bare_extraction, feeds
import lxml
from bs4 import BeautifulSoup
import requests
import PyPDF2
from PyPDF2 import PdfReader
import sys

lan = "de"
#"en", "de"

pdf_directory = f"4_Scraped/{lan}_pdfs"

URL_LIST = f"3_URLs/pdf/urls_{lan}.json"


#Fetch the URL list:
with open(URL_LIST, "r") as new_urls:
    data = json.load(new_urls)


directory = f"4_Scraped/{lan}"
for key, value in data.items():
    try:
        directory_path = directory + "\\" +  key[:2]
        file_path = directory_path+ "\\" + key + ".json"
        if os.path.exists(directory_path):
            if os.path.exists(file_path):
                print(f'{key} exists')
                continue
        else:
            os.makedirs(directory_path)
        try:
            response = requests.get(value)
        except:
            response = requests.get("https://" + value)

        pdf = open(pdf_directory + "\\" + key + ".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        pdffileobj=open(pdf_directory + "\\" + key + ".pdf",'rb')
        pdfreader = PyPDF2.PdfReader(pdffileobj)
        pdf_text = ""
        for i in range(len(pdfreader.pages)):
            page = pdfreader.pages[i].extract_text()
            pdf_text = pdf_text + page
        result = {'title': 'PDF', 'author': 'PDF', 'url': value, 'hostname': 'PDF', 
                'description': 'PDF', 'sitename': 'PDF', 'date': 'PDF', 'id': 'PDF', 
                'license': 'PDF', 'body': 'PDF', 'comments': 'PDF', 'commentsbody': 'PDF', 
                'raw_text': 'PDF', 'text': pdf_text, 'language': 'PDF', 'image': 'PDF', 'pagetype': 'PDF', 'links': 'PDF'}
        with open(file_path, "w") as out_file:
            json.dump(result, out_file)
        print(f'{key} saved')
    except:
        print("error with " + key)
        

