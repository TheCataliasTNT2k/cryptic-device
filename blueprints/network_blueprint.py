from flask import Blueprint, request, Response
from util import make_response
from models.device import Device
from models.network import Network
from models.auth import Session

networks = Blueprint('network', __name__)


@networks.route("/", methods=["PUT"])
def add_device_to_network() -> Response:
    """
    Add a device to network
    """

    # TODO


@networks.route("/", methods=["POST"])
def create_network() -> Response:
    """
    Create a network and returns assigned id
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    user = session.owner

    created_device = Device.create_device(user)
    return make_response(created_device.as_private_simple_dict())


@networks.route("/", methods=["DELETE"])
def delete_network() -> Response:
    """
    Delete a network by id
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    network_id = request.form.get("id")
    if network_id:
        network = Network.get_by_id(network_id)
        network.delete()
    else:
        return make_response({
            "error": "id missing, or not existing"
        })

    return make_response({
        # TODO response needed? Or is missing response allowed?
    })


@networks.route("/", methods=["GET"])
def get_network_info() -> Response:
    """
    Returns data about the target network
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    network_id = request.form.get("id")
    response = dict

    if network_id:
        network_list = [Network.get_by_id(network_id)]
    else:
        network_list = Network.get_by_owner(session.owner)  # TODO check if .all() returns list, else fix to list

    if not network_list:
        return make_response({
            "error": "no networks found"
        })

    for network in network_list:
        if session.owner == network.owner:
            response.update({network.id: network.as_private_simple_dict()})
        else:
            response.update({network.id: network.as_public_simple_dict()})

    return make_response(response)