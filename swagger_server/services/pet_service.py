import os
import re
import sys

from injector import Module, singleton, provider, Injector

from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

from bson.json_util import dumps, CANONICAL_JSON_OPTIONS
import json

COLLECTION = "pets"


class PetService:
    def __init__(self):
        self.username = os.environ.get("MONGO_USERNAME")
        self.password = os.environ.get("MONGO_PASSWORD")
        self.database = os.environ.get("MONGO_DATABASE")
        self.host = os.environ.get("MONGO_HOST")
        self.port = os.environ.get("MONGO_PORT")
        if self.username is None or self.password is None or self.database is None or self.host is None or self.port is None:
            print("Fill the connection settings to connect to MongoDB")
            sys.exit(1)
        self.instance = None

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = MongoClient("%s:%s" % (self.host, str(self.port)),
                             username=self.username,
                             password=self.password,
                             authSource=self.database,
                             authMechanism='SCRAM-SHA-256')
            self.instance[self.database][COLLECTION].create_index('id', unique=True)
        return self.instance[self.database]

    def find_all(self, offset = 0, limit = 0, no_photo = False) -> list:
        db = self.connection()
        display_dict = {'_id': False}
        if no_photo:
            display_dict["photo"] = False
        pets = db[COLLECTION].find({}, display_dict).skip(offset).limit(limit)
        return pets

    def create(self, obj: dict) -> dict:
        db = self.connection()

        while True:

            collection = db[COLLECTION]
            cursor = collection.find(
                {},
                {'id': 1}
            ).sort('id', direction=DESCENDING).limit(1)

            if cursor.count() == 0:
                obj['id'] = 1
            else:
                obj['id'] = cursor.next()['id'] + 1

            try:
                collection.insert_one(obj)
                obj.pop('_id', None)  # _id is not serializable!!!!
            except DuplicateKeyError:
                continue

            break

        return obj

    def delete_one(self, pet_id: int) -> bool:
        db = self.connection()
        deleted_result = db[COLLECTION].delete_one({'id': pet_id})
        return deleted_result.deleted_count == 1

    def find_by_id(self, pet_id: int) -> dict:
        db = self.connection()
        return db[COLLECTION].find_one({'id': pet_id}, {'_id': False})

    def update_or_create(self, pet: dict) -> bool:
        db = self.connection()
        update_result = db[COLLECTION].replace_one({'id': pet.get('id')}, pet, upsert=True)
        return update_result.matched_count == 1

    def update_adoptionspeed(self, pet_id: int, adoption_speed: int) -> bool:
        db = self.connection()
        update_result = db[COLLECTION].update_one({'id': pet_id}, {"$set": {"adoptionSpeed": adoption_speed}}, upsert=True)
        return update_result.matched_count == 1