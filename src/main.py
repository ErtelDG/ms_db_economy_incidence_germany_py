import json
import time, threading
from api import endpointsList, dataList, getDataId
from utils import loadUrl, extractCsvLinks, downloadDataToJson,logFiles, rootPath
from flask import Flask, jsonify, request


def updateRawData():

    while True:
        logFiles.logger.info("Update raw data starts")
        url = None
        while url == None:
            url = loadUrl.load_url_from_env()
            time.sleep(5)
        csv_links = extractCsvLinks.extract_csv_links(url)

        # Check, structure is valid?
        if (csv_links and isinstance(csv_links, dict) and
            all(isinstance(v, dict) and all(isinstance(s, dict) and all(isinstance(p, list) and all(isinstance(link, dict) and 'url' in link for link in p) for p in s.values()) for s in v.values()) for v in csv_links.values())):
            logFiles.logger.info("CSV links structure is valid. Starting download and conversion.")
            downloadDataToJson.download_and_convert_to_json(csv_links)
        else:
            logFiles.logger.error("Invalid CSV links structure.")

        logFiles.logger.info("Update raw data ends")
        time.sleep(2592000)  # 30 days


threatUpdateRawData = threading.Thread(target=updateRawData)


def main():
    threatUpdateRawData.start()

    host='0.0.0.0'
    port=5000

    app = Flask(__name__)

    @app.route(endpointsList.endpoints['/'].get('path'))
    def home():
        return endpointsList.endpoints
        
    
    @app.route(endpointsList.endpoints['/list'].get('path'))
    def getList():
        return dataList.getList()
    

    @app.route(endpointsList.endpoints['/data'].get('path'))
    def getDataID():
        return getDataId.getDataID(request.args.get('id'))
          

    print(f'Server started on: http://{host}:{port}')
    app.run(host, port)

    

if __name__ == "__main__":
    main()
