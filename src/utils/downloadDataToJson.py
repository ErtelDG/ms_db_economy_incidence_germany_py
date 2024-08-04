import datetime
from io import StringIO
from pathlib import Path
import json, os, time, requests
import pandas as pd
from utils import logFiles, rootPath

def cleanup_old_backups(backup_directory, max_backup_count=24):
    """
    Remove old backup directories if more than the maximum allowed exist.
    """
    backup_subdirs = sorted(
        [d for d in os.listdir(backup_directory) if os.path.isdir(os.path.join(backup_directory, d))],
        key=lambda d: os.path.getctime(os.path.join(backup_directory, d))
    )
    
    if len(backup_subdirs) > max_backup_count:
        for old_subdir in backup_subdirs[:len(backup_subdirs) - max_backup_count]:
            old_subdir_path = os.path.join(backup_directory, old_subdir)
            # Remove the old backup directory and its contents
            for root_dir, dirs, files in os.walk(old_subdir_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root_dir, name))
                for name in dirs:
                    os.rmdir(os.path.join(root_dir, name))
            os.rmdir(old_subdir_path)
            logFiles.logger.info(f"Deleted old backup directory: {old_subdir_path}")

def download_and_convert_to_json(structure):
    root = rootPath.get_project_root('root.md')
    data_directory = os.path.join(root, 'src', 'data')
    backup_directory = os.path.join(root, 'src', 'backup')

    # Create the backup directory if it does not exist
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    # Create a timestamped backup folder
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    timestamped_backup_directory = os.path.join(backup_directory, timestamp)
    os.makedirs(timestamped_backup_directory)

    # Move existing files from the data directory to the timestamped backup directory
    if os.path.exists(data_directory):
        for filename in os.listdir(data_directory):
            file_path = os.path.join(data_directory, filename)
            if os.path.isfile(file_path):
                backup_path = os.path.join(timestamped_backup_directory, filename)
                os.rename(file_path, backup_path)
                logFiles.logger.info(f"Moved file to backup: {backup_path}")

    # Ensure the data directory is empty (no need if files are moved above)
    for filename in os.listdir(data_directory):
        file_path = os.path.join(data_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            logFiles.logger.info(f"Removed file from data directory: {file_path}")

    # Remove old backup directories if more than 24 exist
    cleanup_old_backups(backup_directory, max_backup_count=24)

    # Create the data directory if it does not exist
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # Process and save the new data
    for economy_incidence, economy_incidence_content in structure.items():
        for category, category_content in economy_incidence_content.items():
            for subcategory, links in category_content.items():
                for link in links:
                    try:
                        # Download csv
                        response = requests.get(link['url'])
                        time.sleep(2)  # Be polite and avoid overwhelming the server
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
                            json_file_path = os.path.join(data_directory, f'{id}.json')
                            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                                json.dump(result, json_file, ensure_ascii=False, indent=4)

                            logFiles.logger.info(f"Saved file: {json_file_path}")

                    except requests.HTTPError as http_err:
                        logFiles.logger.error(f"HTTP error while downloading: {link['url']}: {http_err}", exc_info=True)
                    except requests.RequestException as req_err:
                        logFiles.logger.error(f"Error downloading file: {link['url']}: {req_err}", exc_info=True)
                    except Exception as e:
                        logFiles.logger.error(f"Error processing file {link['url']}: {e}", exc_info=True)
