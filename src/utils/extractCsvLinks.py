import json
import os
from venv import logger
from bs4 import BeautifulSoup
import requests


def extract_csv_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error: {errh}", exc_info=True)
        return []
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection error: {errc}", exc_info=True)
        return []
    except requests.exceptions.Timeout as errt:
        print(f"Timeout error: {errt}", exc_info=True)
        return []
    except requests.exceptions.RequestException as err:
        print(f"Error while calling: {err}", exc_info=True)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    structure = {}

    h2 = None
    h3 = None
    p = None

    for tag in soup.find_all(['h2', 'h3', 'p', 'a']):
        if tag.name == 'h2':
            h2 = tag.text.strip()
            structure[h2] = {}
        elif tag.name == 'h3' and h2:
            h3 = tag.text.strip()
            structure[h2][h3] = {}
        elif tag.name == 'p' and h2 and h3:
            p = tag.text.strip()
            structure[h2][h3][p] = []
        elif tag.name == 'a' and h2 and h3 and p and tag['href'].endswith('.csv'):
            link_name = tag['href'].split("/")[-1][:-4]
            link_url = tag['href']
            link_title = tag['title'].split('CSV-Datei: ')[-1].strip()
            structure[h2][h3][p].append({
                'name': link_name,
                'url': link_url,
                'title': link_title
            })
    
     # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path for the JSON file
    json_path = os.path.join(script_dir, 'csv_links.json')

    # Save the structure to a JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=4, ensure_ascii=False)

    return structure