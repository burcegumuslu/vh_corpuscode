## Requires installing presidio
#TERMINAL
###pip install presidio_analyzer
###pip install presidio_anonymizer
### python -m spacy download en_core_web_lg
#Further info: https://microsoft.github.io/presidio/getting_started/

#import spacy
#spacy.cli.download("es_core_news_md")

lan = "en"

import os, json
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.predefined_recognizers import EmailRecognizer, IbanRecognizer, PhoneRecognizer, CreditCardRecognizer, MedicalLicenseRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider


configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "es", "model_name": "es_core_news_md"},
        {"lang_code": "en", "model_name": "en_core_web_lg"},
        {"lang_code": "de", "model_name": "de_core_news_md"}
    ],
}

# Create NLP engine based on configuration
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine_multi = provider.create_engine()

registry = RecognizerRegistry()
#registry.load_predefined_recognizers()

#yaml_file = "python/recognizers.yml"

#registry.add_recognizers_from_yaml(yaml_file)

# Set up analyzer with our updated recognizer registry
analyzer = AnalyzerEngine(registry=registry,
    supported_languages=["es", "en", "de"],
    nlp_engine= nlp_engine_multi
    )


def get_chunks(text, chunk_size):
     chunks = [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]
     return chunks

#entities=["PHONE_NUMBER", "PERSON", "CREDIT_CARD", "CRYPTO",
 #                                     "EMAIL_ADDRESS", "IBAN_CODE", "IP_ADDRESS", "MEDICAL_LICENSE", "IBAN", "IBAN_ES"],

def anonimize(text):

    results = analyzer.analyze(text=text,
                            entities=["PHONE_NUMBER", "CREDIT_CARD", "CRYPTO",
                                      "EMAIL_ADDRESS", "IBAN_CODE", "IP_ADDRESS", "MEDICAL_LICENSE"],
                            language="en")
    # DATE_TIME, NRP, LOCATION, URL
    for res in results:
        print(text[res.start:res.end])
    
   # print([(text[res.start:res.end], res.start, res.end) for res in results])

    # Analyzer results are passed to the AnonymizerEngine for anonymization

    anonymizer = AnonymizerEngine()
    anonymized_result = anonymizer.anonymize(text=text,analyzer_results=results)

    serializable_result = anonymized_result.__dict__

    anonymized_text = anonymized_result.text
    return anonymized_text


directory = f"5_Filtered/{lan}"

public =  f"6_PersonalDataRemoved/{lan}"

print(directory)
print(public)

for subdir, dir, files in os.walk(directory):
    for file in files:
        if "json" in file:
            try:
                path = os.path.join(subdir, file)
                new_file = public + f"/{file[:2]}/{file}"
                if os.path.exists(public + f"/{file[:2]}"):   
                    if os.path.exists(new_file):
                        print(file, " exists")
                        continue
                else:
                    os.makedirs(public + f"/{file[:2]}")
                with open(path) as f:
                    data = json.load(f)
                if "text" in data:
                    text = data["text"]
                    anon_text = ""
                    for chunk in get_chunks(text, 1000000):
                        anon_chunk  = anonimize(chunk)
                        anon_text = anon_text + anon_chunk 
                    data["text"] = anon_text
                else: 
                    text = data["cleaned_text"]
                    anon_text = ""
                    for chunk in get_chunks(text, 1000000):
                        anon_chunk  = anonimize(chunk)
                        anon_text = anon_text  + anon_chunk 
                    data["cleaned_text"] = anon_text
                with open(new_file, "w+") as f:
                    json.dump(data, f)
            except:
                print("error with", file)
                
