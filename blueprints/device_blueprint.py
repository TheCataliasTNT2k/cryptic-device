from flask import Blueprint, request, Response
from util import make_response
from models.device import Device
from models.auth import Session

devices = Blueprint('device', __name__)


@devices.route("/", methods=["POST"])
def create_device() -> Response:
    """
    Create a device and returns assigned id
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    address = request.form.get("address")
    user = session.owner
    power = request.form.get("power")
    networks = request.form.get("networks")

    created_device = Device.create_device(user, address, power, networks)
    return make_response(created_device.as_private_simple_dict())


@devices.route("/", methods=["DELETE"])
def delete_device() -> Response:
    """
    Delete device by id
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    device_id = request.form.get("id")
    device = Device.get_by_id(device_id)
    if device_id:
        if session.owner != device.owner:
            return make_response({
                "error": "permission denied"
            })
        device.delete()
    else:
        return make_response({
            "error": "id missing, or not existing"
        })

    return make_response({
     # TODO response needed? Or is missing response allowed?
    })


@devices.route("/", methods=["GET"])
def get_device_info() -> Response:
    """
    Return data about the target device
    """

    token = request.headers.get('Token')
    session = Session.find(token)
    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    device_id = request.form.get("id")
    response = dict

    if device_id:
        device_list = [Device.get_by_id(device_id)]
    else:
        device_list = Device.get_by_owner(session.owner)  # TODO check if .all() returns list, else fix to list

    if not device_list:
        return make_response({
            "error": "no devices found"
        })

    for device in device_list:
        if session.owner == device.owner:
            response.update({device.id: device.as_private_simple_dict()})
        else:
            response.update({device.id: device.as_public_simple_dict()})

    return make_response(response)
