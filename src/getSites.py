import requests
import gzip
import shutil
import os
import time

# Define the URL
url = "https://data.colonialcollections.nl/nmvw/collection-archives/download.trig.gz?graph=https%3A%2F%2Fdata.colonialcollections.nl%2Fnmvw%2Fgraph%2Fsites"

# Define file names
gz_file = "data/sites.trig.gz"
trig_file = "data/sites.trig"

# Step 1: Download the .trig.gz file
print("Downloading file...")
response = requests.get(url, stream=True)
print(os.getcwd())

if response.status_code == 200:
    with open(gz_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print(f"File downloaded: {gz_file}")
    time.sleep(5)

else:
    print(f"Failed to download file. HTTP status code: {response.status_code}")
    exit()

# Step 2: Extract the .trig file
print("Extracting file...")
with gzip.open(gz_file, "rb") as f_in:
    with open(trig_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"Extraction complete: {trig_file}")

# Step 3: Delete the .gz file
os.remove(gz_file)
print(f"Deleted compressed file: {gz_file}")
