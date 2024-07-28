import time
from utils import loadUrl, extractCsvLinks, downloadDataToJson,logFiles


def updateRawData():

    while True:
        logFiles.logger.info("Update raw data starts")
        url = None
        while url == None:
            url = loadUrl.load_url_from_env()
            time.sleep(5)
        links = extractCsvLinks.extract_csv_links(url)
        downloadDataToJson.download_and_convert_to_json(links)
        logFiles.logger.info("Update raw data ends")
        
        time.sleep(2592000)  # 30 Tage

def main():
    updateRawData()   
     

if __name__ == "__main__":
    main()
