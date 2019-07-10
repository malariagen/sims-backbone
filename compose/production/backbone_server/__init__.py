#!/usr/bin/env python3

import connexion

from openapi_server import encoder

def create_app():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Backbone'})

    return app.app

application = create_app()

