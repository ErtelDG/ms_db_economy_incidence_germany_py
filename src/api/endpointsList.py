endpoints = {
        "/": {
            "endpoint": "/",
            "path": "/",
            "title": "home, root",
            "description": "Overview for all endpoints"
        },
        "/list": {
            "endpoint": "/list",
            "path": "/list",
            "title": "Data endpoints",
            "description": "Return an overview of all data endpoints."
        },
        "/data": {
            "endpoint": "/data?<int:id>",
            "path": "/data",
            "title": "Ger data for id. Id as int",
            "description": "Return data as JSON for the request ID"
        }
    }