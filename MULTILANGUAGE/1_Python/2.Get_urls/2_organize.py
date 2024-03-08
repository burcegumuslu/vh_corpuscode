import json, os

###PATHS ARE RELATIVE TO MULTILANGUAGE

url_lists = "3_URLs/raw"

for file in os.listdir(url_lists):
    if ".json" in file:
        path = os.path.join(url_lists, file)
        with open(path, "r") as f:
            data = json.load(f)

        new_data = data.copy()
        pdf_data = {}

        for key,value in data.items():
    
            if value[-4:] == ".pdf":
                pdf_data.update({key:value})
                new_data.pop(key)
        
            try:
                if value[-6] == "xml.gz":
                    new_data.pop(key)
            except:
                pass
            try:
                if value[-9] == ".document":
                    new_data.pop(key)
            except:
                pass
        
        print(len(data))
        print(len(new_data))
        print(len(pdf_data))

        with open(f"3_URLs/html/{file}", "w+") as f:
            json.dump(new_data, f)

        with open(f"3_URLs/pdf/{file}", "w+") as f:
            json.dump(pdf_data, f)


    