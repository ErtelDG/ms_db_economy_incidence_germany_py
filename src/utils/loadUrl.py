import os
import time

from dotenv import load_dotenv
from utils import logFiles

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

def load_url_from_env():

    if not os.path.exists(".env"):
        logFiles.logger.info(f"Create .env file in root")
        with open('.env', 'w') as f:
            f.write("")
  
    if os.path.exists(env_path):
        load_dotenv(env_path)
        url = os.getenv('URL')
        if url:
            logFiles.logger.info(f"URL loaded successfully: {url}")
            return url
        else:
            logFiles.logger.error("No URL found in the .env file.")
            url = prompt_for_valid_url()
            save_url_to_env(url)
            time.sleep(2)
            return None
    else:
        print(".env file not found in root directory.")
        logFiles.logger.error("..env file not found in root directory.")
        return None

def prompt_for_valid_url():
    while True:
        url = input("Please enter a valid URL: ")
        if url.startswith('http://') or url.startswith('https://'):
            print(f"URL is valid, save: {url}")
            logFiles.logger.info(f"URL is valid, save in .env: {url}")
            return url
        else:
            print("Invalid URL. Please try again. Example https://example.com")
            logFiles.logger.error(f"Invalid URL. Please try again. Example https://example.com")

def save_url_to_env(url):
    with open(env_path, 'w') as f:
        f.write(f"URL={url}\n")
    print(f"URL was saved in the .env file: {url}")
    logFiles.logger.info(f"URL was saved in the .env file: {url}")
