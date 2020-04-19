#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_injector import FlaskInjector
from injector import Binder, singleton, Injector
from .services import PetService

def configure(binder: Binder) -> Binder:
    binder.bind(
        PetService,
        to=PetService(),
        scope=singleton
    )



def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.url_map.strict_slashes = False
    app.add_api('swagger.yaml', arguments={'title': 'AdoptACutie'}, pythonic_params=True)
    FlaskInjector(app=app.app, modules=[configure])
    app.run(port=8080)


if __name__ == '__main__':
    main()
