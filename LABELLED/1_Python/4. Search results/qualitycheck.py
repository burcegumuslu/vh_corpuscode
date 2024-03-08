import os
import json

directory = "/Users/burce/Desktop/corpus/python/Search results (Annotated)/SE old"

for filename in os.listdir(directory):
    if 'json' in filename and "mainstream" in filename:
        print(filename)
        file_path = os.path.join(directory, filename)
        with open(file_path) as f:
            data = json.load(f)

        for entry in data:
            if len(entry["results"]) > 60:
                entry["results"] = entry["results"][59]
        with open(file_path, 'w') as f:
            json.dump(data, f)

for filename in os.listdir(directory):
    if 'json' in filename and "mainstream" in filename:
        print(filename)
        file_path = os.path.join(directory, filename)
        with open(file_path) as f:
            new_data = json.load(f)

        for entry in new_data:
            if len(entry["results"]) > 60:
                print(len(entry["results"]))