##Paths are relative to LABELLED

import os, json

subcorpora = {"PS", "TS", "SE"}
    
combined_list = []


def combine_search_results(subcorpus):
    input_dir = f"4_Searches/MERGED/{subcorpus}"
    for filename in os.listdir(input_dir):
        path = os.path.join(input_dir, filename)
        print(path)
        if "json" in filename:
            with open(path, 'r') as f:
                search_engine_results = json.load(f)
                print("search_engine_results len: ", len(search_engine_results))
            for search_engine_result in search_engine_results:
                domain = search_engine_result['domain']
                results = search_engine_result['results']
                key_word = search_engine_result['keyword']
                for result in results:
                    result.update({'keyword':[key_word]})
                    if len(combined_list) > 0 and any(combined_list[i]['URL'] == result['URL'] for i in range(len(combined_list))):
                        for i in range(len(combined_list)):
                            if combined_list[i]['URL'] == result['URL'] and key_word not in combined_list[i]['keyword']:
                                combined_list[i]['keyword'].append(key_word)
                                print("overlap", result)
                    else:  
                        combined_list.append(result)
        
        with open(f'4_Searches/FINAL/{subcorpus}_search_results_for_scrape.json', 'w+') as f:
            json.dump(combined_list, f)





#subcorpus = "SE"

#combine_search_results(subcorpus)
subcorpus = "PS"

combine_search_results(subcorpus)


#subcorpus = "TS"

combine_search_results(subcorpus)