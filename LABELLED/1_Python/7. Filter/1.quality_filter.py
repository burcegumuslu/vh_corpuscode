import os
import json
import spacy
from scipy.ndimage import uniform_filter1d
from numpy import array
from custom_lists import vaccine_words, cam_words
import textdescriptives as td

subcorpora = {"PS", "TS", "SE"}

nlp = spacy.load("en_core_web_sm")
word_list = set(nlp.vocab.strings)

# add more unigrams that are in our corpus but not in en_core_web_sm
custom_words = set(["covid", "covid-19", "vax"] + vaccine_words + cam_words)
word_list.update(custom_words)

window = 20
threshold = 0.6

# create the spacy nlp pipeline
nlp = spacy.blank("en")
# add a component for sentence segmentation
nlp.add_pipe("sentencizer")
# add a component for quality filtering
quality_pipe = nlp.add_pipe("textdescriptives/quality")

# apply the pipeline to the texts

def process_file(file_in):
    with open(file_in, 'r') as f:
         data = json.load(f)
         raw_text = data['cleaned_text'].replace('\n', ' ')
    body = ''
    tokens = raw_text.split()
    is_word = array([1 if x.lower().strip('.,()') in word_list else 0 for x in tokens], dtype='float')
    hits = uniform_filter1d(is_word, size=window, mode='nearest')
    new_text = ""
    for word, hit in zip(tokens, hits):
        if hit >= threshold:
            new_text += word + " "
    new_data = {}
    new_data['result_id'] = data['result_id']
    new_data['URL'] = data['URL']
    new_data['title'] = data['title']
    new_data['authors'] = data['authors']
    new_data['domain'] = data['domain']
    new_data['publish_date'] = data['publish_date']
    new_data["cleaned_text"] = new_text
    new_data['subcorpus'] = data['subcorpus']
    new_data['domain_source'] = data['domain_source']


    return new_data

def process_files(directory):
    counter = 0
    for filename in os.listdir(directory):
        new_data = process_file(os.path.join(directory, filename))
        if len(new_data['cleaned_text'].split()) < 100:
            print(filename, " removed, less than 100 words")
            continue
        if len(new_data['cleaned_text'].split()) > 10000:
            new_data['cleaned_text'] = " ".join(new_data['cleaned_text'].split()[:10000])
            print("First 10000 words taken: " + filename)
        new_directory_path = directory_output + "\\" + subcorpus
        new_file_path = new_directory_path + "\\" + filename
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)
        with open(new_file_path, "w+") as f:
            json.dump(new_data, f)
        if counter % 20 == 0:
            print(counter, new_file_path)
        counter += 1
        if counter % 20 == 0:
            print(counter, filename)


#process_directory(directory_input)

for subcorpus in subcorpora:
    directory_input = f"5.Scraped\\{subcorpus}"
    directory_output = f"5.Filtered\\{subcorpus}"
    process_files(directory_input)
