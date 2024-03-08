import json, os

###paths are relative to LABELLED

CAM_keyword_dict = {
    "natural immunization": "NIM",
    "holistic healing": "HOH",
    "herbal remedies": "HER",
    "homeopathy": "HOM",
    "naturopathy": "NAT",
    "ayurveda": "AYU",
    "aromatherapy": "ARO",
    "spiritual healing ceremony": "SHC",
    "osteopathy": "OST",
    "anthroposophic medicine": "ANT",
    "non-toxic treatments": "NTT",
    "treatment natural ingredients": "TNI",
    "boost immune system": "BIS"
}

vaccine_keyword_dict = {
    "vaccine": "VAC",
    "vaccine side-effects": "VSE",
    "vaccine alternatives": "VAL",
    "vaccine contamination": "VCO",
    "vaccine autism": "VAU",
    "vaccine immune system": "VIS",
    "vaccine infant": "VAI",
    "vaccine safety": "VAS",
    "vaccine efficacy": "VEF",
    "vaccine clinical trials": "VCT",
    "vaccine approval process": "VAP",
    "vaccine children": "CHI",
    "vaccine toxin": "TOX"
}



keyword_dict = CAM_keyword_dict
keyword_dict.update(vaccine_keyword_dict)


def merge(google_results, bing_results, key, tag, subcorpus):
    keyword_tag = key + tag
    counter_1 = 1
    combined_results = []
    for google_result in google_results:
        result_set = set()
        result_set.update(google_result['results'])
        for bing_result in bing_results:
            if google_result['domain'] == bing_result['domain']:
                result_set.update(bing_result['results'])
        counter_2= 1
        URL_list = []
        for element in result_set:
            source = []
            if element in google_result['results']:
                source.append('google')
            for bing_result in bing_results:
                if google_result['domain'] == bing_result['domain'] and element in bing_result['results']:
                    source.append('bing')
            URL_dict = {'result_id': keyword_tag + str(counter_1).zfill(3) + str(counter_2).zfill(3), 'URL': element, 'source': source}  
            URL_list.append(URL_dict)
            counter_2 = counter_2 + 1
        search_dict = {'domain': google_result['domain'], 'domain_id': str(counter_1).zfill(3), 'keyword':google_result['key_word'], 'results': URL_list}
        counter_1 = counter_1 + 1
        combined_results.append(search_dict)
        output_dir = f"4_Searches/MERGED/{subcorpus}"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(output_dir + f'/{keyword_tag}_merged_search_results.json', 'w') as f:
            json.dump(combined_results, f)



subcorpora = {"PS":"", "TS": "M", "SE": "S"}


for subcorpus, key in subcorpora.items():
    for keyword, tag in keyword_dict.items():
        keyword_docs = []
        for file in os.listdir(f"4_Searches/RAW/{subcorpus}"):
            if keyword in file:
                keyword_docs.append(file)
        for doc in keyword_docs:
            if "Bing" in doc:
                path = os.path.join(f"4_Searches/RAW/{subcorpus}", doc)
                with open(path, 'r') as bing:
                    bing_results = json.load(bing)
            if "Google" in doc:
                path = os.path.join(f"4_Searches/RAW/{subcorpus}", doc)
                with open(path, 'r') as google:
                    google_results = json.load(google)
        
        merge(google_results, bing_results, key, tag, subcorpus)
        