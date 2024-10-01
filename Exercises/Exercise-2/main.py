import os
import csv
from pathlib import Path
from bs4 import BeautifulSoup

import requests
import pandas

# Broken link
# URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
CATALOG_URL = "https://catalog.data.gov"
DOWNLOAD_DIR = Path("./downloads")


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

        # download dataset then write locally
        print("downloading dataset...")
        r = requests.get(download_url)
        decoded_content = r.content.decode("utf-8")
        content_reader = csv.reader(decoded_content.splitlines(), delimiter=",")
        with open(DOWNLOAD_DIR / "temperature.csv", "w") as outfile:
            writer = csv.writer(outfile, delimiter=',')
            for row in content_reader:
                writer.writerow(row)

        # find the records with the highest
        df = pandas.read_csv(DOWNLOAD_DIR / "temperature.csv")
        airtemp = df['AirTemp']
        print(airtemp.max())

    except Exception as e:
        print(e)
    print("hello world")


if __name__ == "__main__":
    main()