import json, os
##install trafilatura: pip install trafilatura
###https://trafilatura.readthedocs.io/en/latest/
from trafilatura import fetch_url, extract, bare_extraction, feeds
import lxml
from bs4 import BeautifulSoup



##"en", "de"

def scrape_unlabelled(lan):
    URL_LIST = f"3_URLs/html/urls_{lan}.json"

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
            downloaded = fetch_url(value)
            result =  bare_extraction(downloaded, include_links=True)
            try:
                result.pop("categories")
                result.pop("tags")
                result.pop("fingerprint")
                links = []
                soup = BeautifulSoup(downloaded, "html.parser")
                for link in soup.find_all("a"):
                    links.append(link.get("href"))
                result["links"] = links
                with open(file_path, "w") as file:
                    json.dump(result, file)
                print(f'{key} saved')
            except:
                print(f'{key} error')
        except:
            print(f"{key} passed")
            pass


lan = "en"
scrape_unlabelled(lan)
lan = "es"
scrape_unlabelled(lan)
lan = "de"
scrape_unlabelled(lan)


    
    