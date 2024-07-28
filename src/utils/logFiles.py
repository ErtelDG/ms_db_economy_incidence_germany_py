
# Verzeichnisse und Logdateien definieren
import logging
import os

from utils import rootPath

root = rootPath.get_project_root('root.md')

log_dir = os.path.join(root, 'src', 'log')
log_file = os.path.join(log_dir, 'logfile.log')
error_log_file = os.path.join(log_dir, 'error.log')

# Verzeichnis erstellen, falls nicht vorhanden
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Konfiguration des Loggings
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log-Handler für allgemeine Logs
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Log-Handler für Fehlerlogs
error_handler = logging.FileHandler(error_log_file)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)