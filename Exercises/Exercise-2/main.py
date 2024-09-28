import os
import signal
from pathlib import Path
from bs4 import BeautifulSoup

import requests
import pandas

# Broken link
# URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
CATALOG_URL = "https://catalog.data.gov"
DOWNLOAD_DIR = Path("./downloads")

# def handler(signum, frame):
#     raise Exception("Function timeout")

# # register signal function handler
# signal.signal(signal.SIGALRM, handler)
# signal.alarm(10)

def main():
    if os.path.exists(DOWNLOAD_DIR) == False:
        os.mkdir(DOWNLOAD_DIR)

    try:
        # find temperature dataset
        r = requests.get(CATALOG_URL + "/dataset?res_format=CSV&tags=weather")
        soup = BeautifulSoup(r.content, 'html.parser')
        divs = soup.find_all("div", class_="dataset-content")
        temperature_url = ""
        for d in divs:
            a = d.find("a")
            url = a.get("href")
            if "temperature" in url.lower():
                temperature_url = url
        print("dataset found!")

        # find download link
        r = requests.get(CATALOG_URL + temperature_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        link = soup.find("a", attrs={"data-format": "csv"})
        download_url = link.get("href")
        # download dataset
        r = requests.get(download_url)
        print("downloading dataset...")


    except Exception as e:
        print(e)
    print("hello world")


if __name__ == "__main__":
    main()
