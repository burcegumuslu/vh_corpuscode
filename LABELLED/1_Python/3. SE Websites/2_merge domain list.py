import json, os, csv

search_results_folder = "1_Python/3. SE Websites/search_results"


def merge(file, domain_dict_list):
    with open(file, 'r') as file:
        dicts = json.load(file)


    for dict in dicts:
        for domain in dict['domains']:
            if not any(do['domain'] == domain['domain'] for do in domain_dict_list):
                domain['source'] = [[dict["search-engine"], dict["key_word"]]]
                domain['corpus'] = 'mainstream'
                domain_dict_list.append(domain)
            else:
                for do in domain_dict_list:
                    if do['domain'] == domain['domain']:
                        do['count'] = do['count'] + domain['count']
                        if [dict["search-engine"], dict["key_word"]] not in do['source']:
                            do['source'].append([dict["search-engine"], dict["key_word"]])

    output = "1_Python/3. SE Websites/se_raw_list.json"
    out_file = output

    with open(output, 'w+') as output:
        json.dump(domain_dict_list, output)
    print("Number of domains ", len(domain_dict_list))
    return out_file
    


###Paths are relative to LABELLED folder!!!
path_TS = '3_Websites/TrustedSources.csv'
path_PS = '3_Websites/Pseudoscience.csv'
path_SE = '3_Websites/SearchEngine.json'


def filter_domains(path):
    filtered_list = []
    with open(path) as file:
        se_list = json.load(file)

    for dict in se_list:
        if dict['count'] > 2 and len(dict['source']) > 1:
            filtered_list.append(dict)
    print("filtered list", len(filtered_list))
    return filtered_list



def create_domain_list(my_list):
    TS_domain_list = []
    with open(path_TS,'r') as input_file:  ## If you want to use other domains create a csv file making sure that the domains
            ###################################### are written the first column.

        reader = csv.reader(input_file, delimiter=';')  ## Depending on the csv file, delimiliter might be different, e.g. ';'

        next(reader)  ## This line should be deleted if the csv file doesn't contain any column names.

        for row in reader:
            TS_domain_list.append(row[0])

    print("TS", len(TS_domain_list))

    print(TS_domain_list)

    PS_domain_list = []

    

    with open(path_PS, 'r') as input_file:  ## If you want to use other domains create a csv file making sure that the domains
        ###################################### are written the first column.

        reader = csv.reader(input_file, delimiter=',')  ## Depending on the csv file, delimiliter might be different, e.g. ';'

        next(reader)  ## This line should be deleted if the csv file doesn't contain any column names.

        for row in reader:
            PS_domain_list.append(row[1])

    print("PS", len(PS_domain_list))

    get_rid_of = []

    get_rid_of = TS_domain_list + ['bing.com', 'google.com', 'google.de', 'bing.de'] + PS_domain_list

    new_domain_list= []

    for dict in my_list:
        if dict['domain'] not in get_rid_of:
            new_domain_list.append(dict['domain'])
        else: 
            print("overlap ", dict['domain'])

    new_domain_list = set(new_domain_list)

    new_domain_list = list(new_domain_list)

    print("SE", len(new_domain_list))

    with open(path_SE, 'w+') as output:
        json.dump(new_domain_list, output)

    return(new_domain_list)


domain_dict_list = []
for file in os.listdir(search_results_folder):
    if "json" in file:
        path = os.path.join(search_results_folder, file)
        output = merge(path, domain_dict_list)
print("Merged the search results")
print(output)

my_list = filter_domains(output)
print(len(my_list))
create_domain_list(my_list)