import json
import pandas as pd

def fetch_json(file):
    while True:
        json = ""
        while len(json) == 0 or json[-1] != "}":
            ch = file.read(1)
            if not ch:
                yield None
            json += ch

        # Calling strip because my file has newline characters between the
        # json blobs
        yield json.strip()


business = pd.read_json('C:/Users/Peter Dell/Documents/ML1010-Yelp-Project/JSON-data/yelp_academic_dataset_business.json', lines=True, orient='columns', encoding='utf-8')
ontario = business.loc[business['state'] == 'ON']

filename = 'C:/Users/Peter Dell/Documents/ML1010-Yelp-Project/JSON-data/yelp_academic_dataset_review.json'
d = []

f = open(filename, "r", encoding = "utf-8")

for j in fetch_json(f):
    if j == None: break
    try:
        p = json.loads(j)
        d.append(p)
    except ValueError:
        print("Garbage text, ignore this line")
        pass

f.close()

df = pd.DataFrame(d)

subset = pd.merge(ontario, df, on="business_id", how="inner")

subset.to_csv("subset.csv", index = False)
