import requests
import src.config as cfg
import io
import os
import pandas as pd
import json

os.makedirs("data/transformed", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)

 
# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/
 
# To hit our API, you'll be making requests to:
base_url = cfg.BASE_URL
write_data = []
 
# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
url = base_url + "/api/3/action/package_show"
params = { "id": cfg.PACKAGE_ID}
package = requests.get(url, params = params).json()

# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):
    if resource["datastore_active"]:
        url = base_url + "/datastore/dump/" + resource["id"]
        resource_dump_data = requests.get(url).text
        df = pd.read_csv(io.StringIO(resource_dump_data))
        df.to_parquet("data/transformed/data_parquet.parquet", index=False)
        with open("data/raw/ferry.csv", "w", encoding="utf-8", newline="") as f:
            f.write(resource_dump_data)

        records = df.to_dict(orient="records")
        with open("data/transformed/ferry.json", "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    

