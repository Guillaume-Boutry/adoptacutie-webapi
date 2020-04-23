import connexion
import six
from functools import wraps

from swagger_server.models.api_response import ApiResponse
from swagger_server.models.pet import Pet  # noqa: E501
from swagger_server import util

from flask_injector import inject
from ..services import PetService, PredictService
from bson.json_util import dumps

from connexion import NoContent

def catch_ex(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}, 400
    return wrapped

@inject
@catch_ex
def add_pet(body, pet_service: PetService):  # noqa: E501
    """Add new pet to service

     # noqa: E501

    :param body: Pet object that needs to be added to the service
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
        pet = Pet.from_dict(pet_service.create(body))
        return pet, 201
    return {"error": "Unserializable"}, 405

@inject
@catch_ex
def delete_pet(pet_id, pet_service: PetService):  # noqa: E501
    """Deletes a pet

     # noqa: E501

    :param pet_id: Pet id to delete
    :type pet_id: int

    :rtype: None
    """
    deleted = pet_service.delete_one(pet_id)
    if deleted:
        return NoContent, 204
    else:
        return NoContent, 404

@inject
@catch_ex
def get_pet_by_id(pet_id:int , pet_service: PetService):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param pet_id: ID of pet to return
    :type pet_id: int

    :rtype: Pet
    """
    pet = pet_service.find_by_id(pet_id)
    if not pet:
        return  {"error": "Not found"}, 404
    return Pet.from_dict(pet)

@inject
@catch_ex
def get_pets(pet_service: PetService):  # noqa: E501
    """Get list of pets

     # noqa: E501


    :rtype: None
    """
    return [Pet.from_dict(res) for res in pet_service.find_all()]

@catch_ex
def predict_adoption_speed(pet_id: int, pet_service: PetService, predict_service: PredictService):  # noqa: E501
    """get an animal prediction

     # noqa: E501

    :param pet_id: ID of pet to predict
    :type pet_id: int

    :rtype: None
    """

    pet = pet_service.find_by_id(pet_id)
    if not pet:
        return  {"error": "Not found"}, 404
    pet = Pet.from_dict(pet)
    prediction = predict_service.predict(pet)
    pet.adoption_speed = prediction
    if pet_service.update_adoptionspeed(pet.id, prediction):
        return prediction
    return {"error": "Error while updating pet"}, 500

@inject
@catch_ex
def update_pet(body, pet_service: PetService):  # noqa: E501
    """Update an existing pet

     # noqa: E501

    :param body: Pet object that needs to be added to the service
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
        exists = pet_service.update_or_create(body)
        return NoContent, (200 if exists else 201)
    return {"error": "Unserializable"}, 405

@catch_ex
def upload_file(pet_id, additional_metadata=None, file=None):  # noqa: E501
    """uploads an image

     # noqa: E501

    :param pet_id: ID of pet to update
    :type pet_id: int
    :param additional_metadata: 
    :type additional_metadata: str
    :param file: 
    :type file: strstr

    :rtype: ApiResponse
    """
    return 'do some magic!'
