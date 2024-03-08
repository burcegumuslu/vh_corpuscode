##   SEARCH RESULTS  ##
#### What does the code do:
## This code takes a keyword (e.g. 'vaccine') and a domain (e.g. mercola.com), and searches the 'site:mercola.com vaccine'
## on Google or Bing.Then it retrieves the URLs of the first 40 results. If the number of search results is less than 40, it retrieves all of them.


## Technical notes:
## Running the code requires
##   - installing selenium
##### in the functions.py there are more instructions to how to do so.

import json, time, csv
import datetime
from datetime import date
import pytz

## Choose keyword

## List of the domains
domain_list = []



def choose_subcorpus():
    subcorpus = input("Select subcorpus. PS, TS, SE").lower()
    if not subcorpus == 'ps' and not subcorpus == 'ts' and not subcorpus == 'help' and not subcorpus == "'help'" and not subcorpus == "se":
        choose_subcorpus()
    return subcorpus


search_for = choose_subcorpus()

vaccine_key_words = ["vaccine", "vaccine side-effects","vaccine alternatives","vaccine contamination","vaccine autism","vaccine immune system","vaccine infant", "vaccine safety","vaccine efficacy","vaccine clinical trials","vaccine approval process", "vaccine children","vaccine toxin"]

cam_key_words = ['natural immunization', 'holistic healing', 'herbal remedies', 'homeopathy', 'naturopathy', 'ayurveda','aromatherapy', 'spiritual healing ceremony', 'osteopathy', 'anthroposophic medicine','non-toxic treatments', 'boost immune system', 'treatment natural ingredients']


def choose_keyword():
    keyword = input("Select keyword. To see the list of keywords, write 'Show'").lower()
    if keyword == "show":
        print("CAM Keywords: ", cam_key_words)
        print("Vaccine Keywords: ", vaccine_key_words)
        choose_keyword()
    if not keyword == "show" and keyword not in cam_key_words and keyword not in vaccine_key_words:
        print("You entered a keyword that is not in the keyword list or you made a typo. Please try again. To see the list of keywords, write 'Show'")
        choose_keyword()
    return keyword

key_word = choose_keyword()


if search_for == 'ps':
    with open('3_Websites/Pseudoscience.csv', 'r') as input_file: ## If you want to use other domains create a csv file making sure that the domains
        ###################################### are written the first column.

        reader = csv.reader(input_file, delimiter=',') ## Depending on the csv file, delimiliter might be different, e.g. ';'

        next(reader) ## This line should be deleted if the csv file doesn't contain any column names.

        for row in reader:
            domain_list.append(row[1])

if search_for == "ts":
    with open('3_Websites/TrustedSources.csv',
              'r') as input_file:  ## If you want to use other domains create a csv file making sure that the domains
        ###################################### are written the first column.


        reader = csv.reader(input_file,
                            delimiter=';')  ## Depending on the csv file, delimiliter might be different, e.g. ';'

        next(reader)  ## This line should be deleted if the csv file doesn't contain any column names.

        for row in reader:
            domain_list.append(row[0])

if search_for == "se":
    with open('3_Websites/SearchEngine.json', 'r') as input_file:  ## If you want to use other domains create a csv file making sure that the domains
        ###################################### are written the first column.

        domain_list = json.load(input_file)


print("Domain len: ", len(domain_list))

# Now domain_list contains the domains from which we want to get search results.

def choose_action():
    print('What do you want to do? \n A. Begin retrieving search results  \n B. Continue retrieving search results  \n C. Revise search results')
    print("Write 'Help' if you need help about how to use this code.")
    what_to_do = input("Pick A, B, C or enter 'Help'").lower()
    if not what_to_do == 'a' and not what_to_do == 'b' and not what_to_do == 'help' and not what_to_do == "'help'" and not what_to_do == "c" and not what_to_do == 'series':
        choose_action()
    return what_to_do

what_to_do = choose_action()

if what_to_do == 'help' or what_to_do == "'help'":
    print("What does the code do: \n This code takes a keyword (e.g. 'vaccine') and a domain (e.g. mercola.com), and searches the 'site:mercola.com vaccine' on Google or Bing.Then it retrieves the URLs of the first 40 results. If the number of search results is less than 40, it retrieves all of them.")
    print(" ")
    print("Running the code requires: ")
    print("- installing selenium")
    exit()

if what_to_do == 'c':
    file_name_to_correct = input('Please specify the directory path and file name (including extension) of the file you wish to revise. If the file is located within this project folder, you may simply enter the file name. ')

if what_to_do == 'b':
    file_name_to_continue = input('Please specify the directory path and file name (including extension) of the file where the previous search results are stored. If the file is located within this project folder, you may simply enter the file name. ')

## Search engine URLs (Google or Bing):
google = "https://www.google.com/"
bing = "https://www.bing.com/"

## Choose search engine
input_search_engine = input('Which search engine do you want to use? Please enter "google" or "bing"').lower()
print(input_search_engine)

##instead of this one can just write:
#input_search_engine = 'google'
#or
##input_search_engine = 'bing'

from functions import open_browser, browser_search, get_URLs_in, quit



def set_search_engine(input_search_engine):
    if input_search_engine == 'bing' or input_search_engine == "'bing'":
        search_engine = bing
        return search_engine
    elif input_search_engine == 'google' or input_search_engine == "'google'":
        search_engine = google
        return search_engine
    else:
        input_search_engine = input('Which search engine do you want to use? Please enter EITHER "google" OR "bing"').lower()
        return set_search_engine(input_search_engine)

search_engine = set_search_engine(input_search_engine)

print(search_engine)
if search_engine == bing:
    search_engine_name = 'Bing'
if search_engine == google:
    search_engine_name = 'Google'


print("Subcorpus:", search_for)
print("Keyword: ", key_word)
print('Search engine: ' + search_engine_name)

#print('Keyword: ' + key_word)
if search_engine == google:
    print('The first 40 results (URLs) will be retrieved.')
    print('NOTE: Google search may be interrupted due to CAPTCHA ("Completely Automated Public Turing test to tell Computers and Humans Apart")')
    print('If this happens, you will recive the following error message "There was a problem due to CAPTHCHA. It is recommended to revise the search results when the current process is finished."')
    print('In that case, please run the code again after the process is finished and select option "B" from the first prompt.')
if search_engine == bing:
    print('The results (URLs) in the first 4 pages will be scraped: If no result is removed first 40 results will be retrieved.')


outfile_name = f"4_Searches/RAW/{search_for}/{search_for}_search_results_{search_engine_name}_{date.today()}_{key_word}.json"
print(outfile_name)

def get_search_results(key_word, search_engine):
    print("DOmain list: ", domain_list)
    search_results = []
    for domain in domain_list:
        domain_result_list = []
        domain_result_dict = {}

        results_removed = False ### Bing sometimes removes results and explicitly states this. This is added
        ########################### to collect that information.

        search_phrase = 'site:' + domain + ' ' + key_word
        print('\n Searching for:')
        print(search_phrase)

        ## Opens the browser and the search engine website that was picked
        open_browser(search_engine)

        ## Searches for the search_phrase that is in the "site:example.com keyword" format
        browser_search(search_engine_name, search_phrase)

        ##### Here what is important is running the get_URLs_in function.
        ##### get_URLs_in returns a Boolean function that indicates whether results were removed or not.
        if search_for == 'CAM':
            results_removed = get_URLs_in(search_engine_name, 4, domain_result_list, results_removed)
        if search_for == 'mainstream YouGov' or search_for == 'mainstream SE':
            results_removed = get_URLs_in(search_engine_name, 6, domain_result_list, results_removed)

        ## Timestamp today
        utc_now = datetime.datetime.now(tz=pytz.utc)
        ## Convert UTC to Germany timezone
        germany_tz = pytz.timezone('Europe/Berlin')
        germany_now = utc_now.astimezone(germany_tz)
        ## Format the timestamp string
        timestamp = germany_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')

        ##UPDATE domain_result_dict
        ## domain_result_dict is different for each domain in our domain list
        if search_engine == bing:
            domain_result_dict = {'domain': domain, 'key_word': key_word, 'results': domain_result_list,
                              'timestamp': timestamp, 'search-engine': search_engine_name, 'results_removed': results_removed}
        if search_engine == google:
            domain_result_dict = {'domain': domain, 'key_word': key_word, 'results': domain_result_list,
                                  'timestamp': timestamp, 'search-engine': search_engine_name,}



        ## UPDATE search_results, this is the list which stores all the information
        search_results.append(domain_result_dict)

        ## To get the results saved in a JSON file:

        with open(outfile_name, "w+") as outfile:
            json.dump(search_results, outfile) #saves the  search_results list as a JSON file. The list is updated
            #### after the search is finished for each domain. So, if there is a problem, the search results from the previous domains
            #### will not be lost
        print(len(domain_result_dict['results']))
        print(" ")
        print("Results are saved in the file:")
        print(outfile_name)

        print("You will need this file name if you want to continue retrieving results or revise the search results")
        time.sleep(2)

    quit()  # shuts down the entire browser


def get_remaining_domains():
    local_domain_list = []
    with open(file_name_to_continue, 'r') as file:
        data = file.read()
        search_results = json.loads(data)
        for domain in domain_list:
            if all(dictionary['domain'] != domain for dictionary in search_results):
                local_domain_list.append(domain)
    return local_domain_list

def continue_getting_search_results(local_domain_list):
    with open(file_name_to_continue, 'r') as file:
        data = file.read()
        search_results = json.loads(data)
        for domain in local_domain_list:
            domain_result_list = []
            domain_result_dict = {}

            results_removed = False  ### Bing sometimes removes results and explicitly states this. This is added
            ########################### to collect that information.

            search_phrase = 'site:' + domain + ' ' + key_word
            print('\n Searching for:')
            print(search_phrase)
            ## Opens the browser and the search engine website that was picked
            open_browser(search_engine)
            ## Searches for the search_phrase that is in the "site:example.com keyword" format
            browser_search(search_engine_name, search_phrase)

            ##### Here what is important is running the get_URLs_in function.
            ##### get_URLs_in returns a Boolean function that indicates whether results were removed or not.
            if search_for == 'CAM':
                results_removed = get_URLs_in(search_engine_name, 4, domain_result_list, results_removed)
            if search_for == 'mainstream YouGov' or search_for == 'mainstream SE':
                results_removed = get_URLs_in(search_engine_name, 6, domain_result_list, results_removed)

            ## Timestamp today
            utc_now = datetime.datetime.now(tz=pytz.utc)
            ## Convert UTC to Germany timezone
            germany_tz = pytz.timezone('Europe/Berlin')
            germany_now = utc_now.astimezone(germany_tz)
            ## Format the timestamp string
            timestamp = germany_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')

            ##UPDATE domain_result_dict
            ## domain_result_dict is different for each domain in our domain list
            if search_engine == bing:
                domain_result_dict = {'domain': domain, 'key_word': key_word, 'results': domain_result_list,
                                      'timestamp': timestamp, 'search-engine': search_engine_name,
                                      'results_removed': results_removed}
            if search_engine == google:
                domain_result_dict = {'domain': domain, 'key_word': key_word, 'results': domain_result_list,
                                      'timestamp': timestamp, 'search-engine': search_engine_name, }

            print(domain_result_dict)

            ## UPDATE search_results, this is the list which stores all the information
            search_results.append(domain_result_dict)

            ## To get the results saved in a JSON file:

            with open(outfile_name, "w+") as outfile:
                json.dump(search_results, outfile)  # saves the  search_results list as a JSON file. The list is updated
                #### after the search is finished for each domain. So, if there is a problem, the search results from the previous domains
                #### will not be lost
            print(len(domain_result_dict['results']))
            print(" ")
            print("Results are saved in the file:")
            print(outfile_name)

            print("You will need this file name if you want to continue retrieving results or revise the search results")
            #time.sleep(2)
        quit()  # shuts down the entire browser




def correct_search_results():
    with open(file_name_to_correct, 'r') as file:
        data = file.read()
        search_results = json.loads(data)
    for dictionary in search_results:
        results_removed = False
        if isinstance(dictionary['results'], list) and None in dictionary['results']:
            domain_result_list = []
            search_phrase = 'site:' + dictionary['domain'] + ' ' + key_word
            print('\n Searching for:')
            print(search_phrase)
            open_browser(search_engine)
            browser_search(search_engine_name, search_phrase)
            if search_for == 'CAM':
                results_removed = get_URLs_in(search_engine_name, 4, domain_result_list, results_removed)
            if search_for == 'mainstream YouGov' or search_for == 'mainstream SE':
                results_removed = get_URLs_in(search_engine_name, 6, domain_result_list, results_removed)
            utc_now = datetime.datetime.now(tz=pytz.utc)
            # Convert UTC to Germany timezone
            germany_tz = pytz.timezone('Europe/Berlin')
            germany_now = utc_now.astimezone(germany_tz)
            # Format the timestamp string
            timestamp = germany_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            dictionary['results'] = domain_result_list
            print(dictionary)

            with open(outfile_name, 'w+') as outfile:
                # Use the json.dump() method to write the dictionaries as separate JSON objects
                json.dump(search_results, outfile)

            print(" ")
            print("Results are saved in the file:")
            print(outfile_name)
            print("You will need this file name if you want to continue retrieving results or revise the search results")
            time.sleep(2)
    quit()  # shuts down the entire browser


if what_to_do == 'a':
    print("I don't see 0")
    get_search_results(key_word,search_engine)
    print("I don't see 1")
if what_to_do == 'b':
    local_domain_list = get_remaining_domains()
    continue_getting_search_results(local_domain_list)
if what_to_do == 'c':
    correct_search_results()
