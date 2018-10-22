from flask import Blueprint, request, Response
from models.session import Session
from models.user import User
from util import make_response
import string

auth = Blueprint('auth', __name__)


@auth.route("/", methods=["GET"])
def information() -> Response:
    """
    Returns the current session informations by the auth-token

    :return: The current session with informations of owner
    """

    token = request.headers.get('Token')

    session = Session.find(token)

    if session is None:
        return make_response({
            "error": "token does not exists"
        })

    return make_response({
        "session": session.as_simple_dict(),
        "user": User.get_by_id(session.owner).as_private_simple_dict()
    })


@auth.route("/", methods=["POST"])
def login() -> Response:
    """
    Handles the login which means that this will create a new session
    if the given credentials are valid.

    :return: A response
    """

    token = request.headers.get('Token')

    username = request.form.get("username")
    password = request.form.get("password")

    # check if username and password are given
    if None in (username, password):
        return make_response({
            "error": "username or password not given"
        })

    # checks if the token sent by the user does exist and is still valid
    if token is not None:
        session = Session.find(token)
        if session is not None:
            if session.is_valid():
                return make_response({
                    "error": "already signed in"
                })

    user = User.get(username)
    if not user:
        return make_response({
            "error": "incorrect password"
        })

    password_validity = user.validate_password(password)

    if password_validity:
        return make_response({
            # create session and return its token
            "token": Session.create(user.id).token
        })
    else:
        return make_response({
            "error": "incorrect password"
        })


@auth.route("/", methods=["DELETE"])
def logout() -> Response:
    """
    This deletes a session.

    :return: A response
    """

    token = request.headers.get('Token')

    if token is None:
        return make_response({
            "error": "no token given"
        })

    session = Session.find(token)

    if session is None:
        return make_response({
            "error": "can not log out from nothing"
        })

    # find session and delete it
    Session.find(token).delete()

    # send "ok"
    return make_response({
        "ok": True
    })


@auth.route("/", methods=["PUT"])
def register() -> Response:
    """
    Registers a new user.

    :return: Returns a response.
    """

    # Get form values
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if None in (username, password, email):
        return make_response({
            "error": "something is missing"
        })

    # Check if the username is already taken
    if User.exists_username(username):
        return make_response({
            "error": "username is already taken"
        })

    specialchars = '!§$%&/()=?+*~#,.;:_-^°<>|\@€'
    passwordchars = list(password)

    s = 0
    u = 0
    l = 0
    d = 0
    for char in passwordchars:
        if char in specialchars:
            s = 1
    if s != 1:
        return make_response({
            "error": "you need at least one special character in your password"
        })
    for char in passwordchars:
        if char in string.digits:
            d = 1
    if d != 1:
            return make_response({
                "error": "you need at least one digit in your password"
            })
    for char in passwordchars:
        if char in string.ascii_uppercase:
            u = 1
    if u != 1:
        return make_response({
            "error": "you need at least one uppercase character"
        })
    for char in passwordchars:
        if char in string.ascii_lowercase:
            l = 1
    if l != 1:
        return make_response({
            "error": "you need at least one lowercase character"
        })

    # Check if the password is longer than 8 chars
    if len(password) < 9:
        return make_response({
            "error": "password is too short (at least 8 characters)"
        })

    # Check if the email is already used
    if User.exists_email(email):
        return make_response({
            "error": "email is already being used"
        })

    # TODO validate email

    User.create(username, password, email)

    return make_response({
        "created": True
    })
