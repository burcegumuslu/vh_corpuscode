import json, os
import unicodedata
import os, json, spacy, re
import textdescriptives as td
from scipy.ndimage import uniform_filter1d
from numpy import array
from custom_lists import vaccine_words, cam_words
import os, json, spacy, re
import textdescriptives as td
from scipy.ndimage import uniform_filter1d
from numpy import array
from custom_lists import vaccine_words, cam_words

#Terminal: python -m spacy download de_core_news_sm

lan = "de"

directory_input = f"4_Scraped/{lan}"
directory_output = f"5_Filtered/{lan}"
info_output = f"1_Python/4. Filter/{lan}"

error_list = []

def is_all_digits(input_string):
    return input_string.isdigit()

def replace_unicode(text):
    # spaces
    #replace punctuation
    text = text.replace('\\u2019', "\'")
    text = text.replace('\\u2018', "\'")
    text = text.replace('\\u2013', '-')
    text = text.replace('\\u201d', '\\"')
    text = text.replace('\\u201c', '\\"')
    text = text.replace('\\u2014', '—')
    text = text.replace('\\u2026', '...')
    text = text.replace('\\u0021', '!')
    text = text.replace('\\u002e', '.')
    text = text.replace('\\u0022', '\\"')
    text = text.replace('\\u0027', "\'")
    text = text.replace('\\u002c', ',')
    text = text.replace('\\ucfb01', 'fi')
    text = text.replace('\\ufb02', 'fl')

    #replace letters
    text = text.replace('\\u00e9', 'é')
    text = text.replace('\\u00fc', 'ü')
    text = text.replace('\\u00e4', 'ä')
    text = text.replace('\\u00e1', 'á')
    text = text.replace('\\u00f6', 'ö')
    text = text.replace('\\u00f3', 'ó')
    text = text.replace('\\u00ed', 'í')
    text = text.replace('\\u20ac', '€')
    text = text.replace('\\u00f1', 'ñ')
    text = text.replace('\\u00d3', 'Ó')
    text = text.replace('\\u00cd', 'Í')
    text = text.replace('\\u00c1', 'Á')
    text = text.replace('\\u00c9', 'É')
    text = text.replace('\\u00e7', 'ç')
    text = text.replace('\\u00e3', 'ã')
    text = text.replace('\\u00bf', '¿')
    text = text.replace('\\u00d1', 'Ñ')
    text = text.replace('\\u00da', 'Ú')
    text = text.replace('\\u00e8', 'è')
    text = text.replace('\\u00e0', 'à')
    text = text.replace('\\u00ea', 'ê')
    text = text.replace('\\u00c3', 'Ã')
    text = text.replace('\\u00f5', 'õ')
    text = text.replace('\\u043e', 'o')
    text = text.replace('\\u0430', 'a')
    text = text.replace('\\u0435', 'e')
    text = text.replace('\\u00e2', 'â')  
    text = text.replace('\\u00f2', 'ò') 
    text = text.replace('\\u00f4', 'e')


    #pattern = r'\\u[0-9A-Fa-f]{4}'
    pattern = r'\\u[0-9A-Fa-f]{4}'
    matches = re.findall(pattern, text)
    for match in list(set(matches)):
        #print(match[2:5])
        if  is_all_digits(match[2:4]) and int(match[2:4]) == 0:
            #print(match, "kept")
            continue
        if is_all_digits(match[2:5]) and int(match[2:5]) < 7:
            #print(match, "kept")
            continue
        if is_all_digits(match[2:5]) and 80 < int(match[2:5]) < 90:
            #print(match, "kept")
            continue
        if  is_all_digits(match[2:4]) and int(match[2:4]) == 20 and (match[3].lower() == "a" or match[3].lower() == "b" or match[3].lower() == "c"):
            #print(match, "kept")
            continue
        else:
            text = text.replace(match, '')
            #print(match, "removed")

   # print(text)
    return text

def process_raw_file(file_in):
    #print(file_in)
    with open(file_in, 'r') as f:
        raw_text = f.read()
    return  replace_unicode(raw_text)

def filter_unicode(text):
    if text is None:
        return None
    
    filtered_text = ''
    new_char = ''
    for char in text:
        if char is None:
            continue
        for i in range(len(char)):
            code_points = [ord(char[i]) for i in range(len(char))]
            print(code_points)
            for code_point in code_points:
                if (
                    (0x0000 <= code_point <= 0x007F) or  # Basic Latin
                    (0x0080 <= code_point <= 0x00FF) or  # Latin-1 Supplement
                    (0x20A0 <= code_point <= 0x20CF) #or  # Latin Extended-A
                    #(0x0180 <= code_point <= 0x024F) or   # Latin Extended-B
                    #(0x0250 <= code_point <= 0x02AF) 
                ):
                    new_char += char[i]
                #else:
                 #   print(char[i])
        filtered_text += char
    return filtered_text


if lan == "en":
    language_model = "en_core_web_sm"
if lan == "es":
    language_model = "es_core_news_sm"
if lan == "de":
    language_model = "de_core_news_sm"


nlp = spacy.load(language_model)
word_list = set(nlp.vocab.strings)

# add more unigrams that are in our corpus but not in en_core_web_sm
custom_words = set(["covid", "covid-19", "vax"]  + vaccine_words + cam_words)
word_list.update(custom_words)

window = 20
threshold = 0.6


# create the spacy nlp pipeline
nlp = spacy.blank(f"{lan}")
# add a component for sentence segmentation
nlp.add_pipe("sentencizer")
# add a component for quality filtering
quality_pipe = nlp.add_pipe("textdescriptives/quality")

def get_chunks(text, chunk_size):
     chunks = [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]
     return chunks

def quality_filter(data):
    raw_text = data['text']
    body = ''
    tokens = raw_text.split()
    is_word = array([1 if x.lower().strip('.,()') in word_list else 0 for x in tokens], dtype='float')
    hits = uniform_filter1d(is_word, size=window, mode='nearest')
    new_text = ""
    #garbage = []
    for word, hit in zip(tokens, hits):
        if hit >= threshold:
            #quality = 'ok'
            new_text += word + " "
        #else: 
            #quality = "garbage"
         #   garbage.append(index)
    new_data = {}
    new_data["cleaned_text"] = new_text
    new_data['is_word'] = list(is_word)
    new_data['running_average_quality'] = list(hits)

    return new_data


def quality_filter_labelled(data):
    raw_text = data['cleaned_text']
    body = ''
    tokens = raw_text.split()
    is_word = array([1 if x.lower().strip('.,()') in word_list else 0 for x in tokens], dtype='float')
    hits = uniform_filter1d(is_word, size=window, mode='nearest')
    new_text = ""
    #garbage = []
    for word, hit in zip(tokens, hits):
        if hit >= threshold:
            #quality = 'ok'
            new_text += word + " "
        #else: 
            #quality = "garbage"
         #   garbage.append(index)
    new_data = {}
    new_data["cleaned_text"] = new_text
    new_data['is_word'] = list(is_word)
    new_data['running_average_quality'] = list(hits)

    return new_data

def process_directory(directory):
    counter = 0
    for subdir, dirs, files in os.walk(directory_input):
        for filename in files:
            try: 
                new_directory_path = directory_output + "\\" +  filename[:2]
                new_file_path = new_directory_path + "\\" + filename
                info_directory_path = info_output + "\\" +  filename[:2]
                info_file_path = info_directory_path + "\\" + filename
                if not os.path.exists(info_directory_path):
                    os.makedirs(info_directory_path)
                if not os.path.exists(new_directory_path):
                    os.makedirs(new_directory_path)
                if os.path.exists(new_file_path):
                    print(f'{filename} exists')
                    continue
                first_step = process_raw_file(os.path.join(subdir, filename))
                with open(new_file_path, "w+") as f:
                    f.write(first_step)
                with open(new_file_path, "r") as f:
                    data = json.load(f)
                new_data = quality_filter(data)
                if len(new_data['cleaned_text'].split()) < 100:
                    os.remove(new_file_path)
                    print("Removed " + filename + "Wordcount = " + str(len(new_data['cleaned_text'].split())))
                    continue
                if len(new_data['cleaned_text'].split()) > 10000:
                    new_data['cleaned_text'] = " ".join(new_data['cleaned_text'].split()[:10000])
                    print("First 10000 words taken: " + filename)
                third_step = {}
                third_step['title'] = data['title']
                third_step['author'] = data['author']
                third_step['url'] = data['url']
                third_step['hostname'] = data['hostname']
                third_step['description'] = data['description']
                third_step['sitename'] = data['sitename']
                third_step['date'] = data['date']
                third_step["cleaned_text"] = new_data['cleaned_text']

                info_dict = {}
                info_dict['is_word'] = new_data['is_word']
                info_dict['running_average_quality']  = new_data['running_average_quality'] 
                with open(new_file_path, "w+") as f:
                    json.dump(third_step, f)
                with open(info_file_path, "w+") as f:
                    json.dump(info_dict, f)
                
                print(counter, filename)
                if counter % 20 == 0:
                    with open(f"{lan}_error_list_process_quality.json", "w") as el:
                        json.dump(error_list, el)
                counter +=1
            except:
                print("error with: ", filename)
                error_list.append(filename)
                if counter % 20 == 0:
                    print(counter, filename)
                    with open(f"{lan}_error_list_process_quality.json", "w") as el:
                        json.dump(error_list, el)
                counter +=1
           




process_directory(directory_input)

print(error_list)




