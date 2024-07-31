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
        links = extractCsvLinks.extract_csv_links(url)
        downloadDataToJson.download_and_convert_to_json(links)
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
