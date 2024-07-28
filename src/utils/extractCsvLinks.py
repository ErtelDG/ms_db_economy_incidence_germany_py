from venv import logger
from bs4 import BeautifulSoup
import requests


def extract_csv_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP error: {errh}", exc_info=True)
        return []
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Connection error: {errc}", exc_info=True)
        return []
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout error: {errt}", exc_info=True)
        return []
    except requests.exceptions.RequestException as err:
        logger.error(f"Error while calling: {err}", exc_info=True)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', title=True, href=True)
    csv_links = {}
    for link in links:  
        if link['href'].endswith('.csv'):
            link_name = link['href'].split("/")[-1][:-4]
            link_url = link['href']
            link_title = link['title'].split('CSV-Datei: ')[-1].strip()
            csv_links[link_name] = {'url':link_url, 'title':link_title}
    return csv_links