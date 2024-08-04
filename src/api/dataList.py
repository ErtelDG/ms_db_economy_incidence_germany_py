import json, os
from flask import jsonify

from utils import rootPath


def getList():
        # Das Verzeichnis mit den JSON-Dateien
        root = rootPath.get_project_root('root.md')
        directory = os.path.join(root, 'src', 'data')

         # Dictionary, um die Inhalte der JSON-Dateien zu speichern
        dict_contents = {}
        try:
            # Iteriere durch alle Dateien im Verzeichnis
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'r') as file:
                        try:
                            # Lade den Inhalt der JSON-Datei
                            json_content = json.load(file)
                            # Extrahiere id, title und name und füge sie dem dict_contents hinzu
                            id = str(json_content['id'])
                            rootCategory = str(json_content['economy_incidence'])
                            category = str(json_content['category'])
                            subcategory = str(json_content['subcategory'])
                            title = json_content['title']
                            nameJson = json_content['nameJson']
                            dict_contents[nameJson] = {
                            "id":id,
                            "rootCategory": rootCategory,
                            "category": category,
                            "subcategory":subcategory,
                            "title": title,
                            "nameJson": nameJson
                            }
                        except json.JSONDecodeError as e:
                            return jsonify({"error": f"Fehler beim Laden von {file_path}: {e}"}), 400
                        except KeyError as e:
                            return jsonify({"error": f"Fehler beim Verarbeiten von {file_path}: Schlüssel {e} fehlt"}), 400
        except FileNotFoundError as e:
            return jsonify({"error": f"Verzeichnis nicht gefunden: {e}"}), 404
        except Exception as e:
            return jsonify({"error": f"Ein unerwarteter Fehler ist aufgetreten: {e}"}), 500

        # Rückgabe der gesammelten Inhalte als JSON
        return jsonify(dict_contents), 200