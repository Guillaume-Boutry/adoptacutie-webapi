#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_injector import FlaskInjector
from flask_cors import CORS
from injector import Binder, singleton, Injector
from .services import PetService, PredictService

def configure(binder: Binder) -> Binder:
    binder.bind(
        PetService,
        to=PetService(),
        scope=singleton
    )
    binder.bind(
        PredictService,
        to=PredictService(),
        scope=singleton
    )



def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.url_map.strict_slashes = False
    app.add_api('swagger.yaml', arguments={'title': 'AdoptACutie'}, pythonic_params=True)
    FlaskInjector(app=app.app, modules=[configure])
    CORS(app=app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
