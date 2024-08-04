from io import StringIO
from pathlib import Path
import json, os, time, requests
import pandas as pd
from utils import logFiles, rootPath


def download_and_convert_to_json(structure):
    root = rootPath.get_project_root('root.md')
    directory = os.path.join(root, 'src', 'data')

    if not os.path.exists(directory):
        os.makedirs(directory)

    for economy_incidence, economy_incidence_content in structure.items():
        for category, category_content in economy_incidence_content.items():
            for subcategory, links in category_content.items():
                for link in links:
                    try:
                        # Download csv
                        response = requests.get(link['url'])
                        time.sleep(2)
                        response.encoding = 'utf-8'

                        if response.status_code == 200:
                            data = StringIO(response.text)
                            
                            # Read csv   
                            try:
                                df = pd.read_csv(data, skiprows=1, delimiter=';', decimal=',')
                            except pd.errors.ParserError:
                                data.seek(0)  
                                df = pd.read_csv(data, delimiter=';', decimal=',')
                            
                            # Convert DataFrame to JSON
                            json_data = df.to_json(orient='records', force_ascii=False)

                            # Save data in JSON
                            json_objects = json.loads(json_data)
                            id = int(str(time.time()).replace('.', ''))
                            result = {
                                "id": id,
                                "economy_incidence": economy_incidence,
                                "category": category,
                                "subcategory": subcategory,
                                "nameJson": link['name'],
                                "url": link['url'],
                                "title": link['title'],
                                "data": json_objects
                            }
                            
                            # Save JSON
                            json_file_path = os.path.join(directory, f'{id}.json')
                            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                                json.dump(result, json_file, ensure_ascii=False, indent=4)

                            logFiles.logger.info(f"Saved file: {json_file_path}")

                    except requests.HTTPError as http_err:
                        logFiles.logger.error(f"HTTP error while downloading: {link['url']}: {http_err}", exc_info=True)
                    except requests.RequestException as req_err:
                        logFiles.logger.error(f"Error downloading file: {link['url']}: {req_err}", exc_info=True)
                    except Exception as e:
                        logFiles.logger.error(f"Error processing file {link['url']}: {e}", exc_info=True)