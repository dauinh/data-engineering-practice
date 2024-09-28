import requests, zipfile, os, shutil
from io import BytesIO
from pathlib import Path

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

DOWNLOAD_DIR = Path("./downloads")

def main():
    # 1. create the directory downloads if it doesn't exist
    if os.path.exists(DOWNLOAD_DIR) == False:
        os.mkdir(DOWNLOAD_DIR)

    # 2. download the files one by one.
    for url in download_uris:
        r = requests.get(url)
        # 3. split out the filename from the uri, so the file keeps its original filename.
        filename = url.split("/")[-1][:-4]
        try:
            zfile= zipfile.ZipFile(BytesIO(r.content))
            zfile.extractall(DOWNLOAD_DIR / filename)
            print(f"downloading {filename}...")
        except zipfile.BadZipFile:
            print(f"failed to download {filename}")

        # 4. Each file is a zip, extract the csv from the zip and delete the zip file.
        try:
            csv_file = filename + ".csv"
            shutil.move(DOWNLOAD_DIR / filename / csv_file, DOWNLOAD_DIR / csv_file)
            shutil.rmtree(DOWNLOAD_DIR / filename)
        except FileNotFoundError:
            print(f"{csv_file} doesn't exist")


    print("hello world")


if __name__ == "__main__":
    main()
