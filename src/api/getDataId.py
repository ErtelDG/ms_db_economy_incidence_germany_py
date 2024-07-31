import json
import os
from flask import jsonify, request
from utils import rootPath


def getDataID(id):
        if not id:
            return jsonify({"error": "ID is required"}), 400
        
        root = rootPath.get_project_root('root.md')
        directory = os.path.join(root, 'src', 'data')

        file_path = os.path.join(directory, f'{id}.json')

        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        with open(file_path, 'r') as file:
            data = json.load(file)

        return jsonify(data)