import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.pet import Pet  # noqa: E501
from swagger_server import util


def add_pet(body):  # noqa: E501
    """Add new pet to service

     # noqa: E501

    :param body: Pet object that needs to be added to the service
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Pet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_pet(pet_id, api_key=None):  # noqa: E501
    """Deletes a pet

     # noqa: E501

    :param pet_id: Pet id to delete
    :type pet_id: int
    :param api_key: 
    :type api_key: str

    :rtype: None
    """
    return 'do some magic!'


def get_pet_by_id(pet_id):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param pet_id: ID of pet to return
    :type pet_id: int

    :rtype: Pet
    """
    return 'do some magic!'


def get_pets():  # noqa: E501
    """Get list of pets

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def predict_adoption_speed(pet_id):  # noqa: E501
    """get an animal prediction

     # noqa: E501

    :param pet_id: ID of pet to predict
    :type pet_id: int

    :rtype: None
    """
    return 'do some magic!'


def update_pet(body):  # noqa: E501
    """Update an existing pet

     # noqa: E501

    :param body: Pet object that needs to be added to the service
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Pet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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
