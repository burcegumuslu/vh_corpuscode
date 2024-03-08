import datetime
import traceback
from datetime import date
import pytz
import json, os
###INSTALL GOOSE3: pip install goose3
###https://pypi.org/project/goose3/
from goose3 import Goose
from goose3 import Configuration
import lxml


###Paths are relative to LABELLED 


config = Configuration()
config.browser_user_agent = 'We are retrieving content for non-commercial academic purposes. Contact: cmmock23@gmail.com'
###

g = Goose(config)

#g = Goose()

##Note: IT IS NORMAL TO GET SOME ERRORS IN THE BEGINNING.


def scrape(subcorpus):
    directory = f"5_Scraped/{subcorpus}"
    input_file = f"4_Searches/FINAL/{subcorpus}_search_results_for_scrape.json"
    with open(input_file, "r") as f:
        data = json.load(f)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for dictionary in data:
        result_id = dictionary["result_id"]
        path = os.path.join(directory, result_id + ".json")
        if os.path.exists(path):
            print(result_id, " exists")
            continue
        URL = dictionary['URL']
        try:
            ## Timestamp today
            utc_now = datetime.datetime.now(tz=pytz.utc)
            ## Convert UTC to Germany timezone
            germany_tz = pytz.timezone('Europe/Berlin')
            germany_now = utc_now.astimezone(germany_tz)
            ## Format the timestamp string
            timestamp = germany_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            item_dict = {'result_id': result_id, 'URL': URL, 'timestamp': timestamp}
            article = g.extract(url=URL)
            infos = article.infos
            infos['meta']['website_keywords'] = infos['meta'].pop('keywords')
            item_dict.update(infos)
            #item_dict.update({'raw_html': article.raw_html})
            with open(f'{directory}/{dictionary["result_id"]}.json', 'w+') as output_file:
                json.dump(item_dict, output_file)
            print('Finished with', URL)
        except Exception as e:
            print("There was an error with scraping", URL)
            print(f"Error: {e}")
            traceback.print_exc()

scrape("TS")

scrape("PS")

scrape("SE")
