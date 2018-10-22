from database import db
from models.device import Device


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    owner = db.Column(db.Integer, nullable=False)

    def __init__(self, owner):
        self.owner = owner

    def delete(self) -> None:
        """
        Deletes this device.

        :return: None
        """

        db.session.delete(self)
        self.commit()

    def commit(self) -> None:
        """
        Commits changes to the database.

        :return: None
        """

        db.session.commit()

    @staticmethod
    def create(user) -> 'Network':
        """
        Creates a new network for a specified user.

        :param user: The owner's id
        :return: New device
        """

        network = Network(user)

        db.session.add(network)
        db.session.commit()

        return network

    def add_device(self, device: Device):
        self.devices.append(device)
        self.commit()

    def as_private_simple_dict(self) -> dict:
        """
        Returns a dictionary with basic PRIVATE information about this device.
        :return: dictionary with basic information
        """

        return {
            "network_id": self.id,
            "network_owner": self.owner
        }

    def as_public_simple_dict(self) -> dict:
        """
        Returns a dictionary with basic PUBLIC information about this device.
        :return: dictionary with basic information
        """

        return {
            "network_id": self.id,
            "network_owner": self.owner

        }

    @staticmethod
    def get_by_id(id: int) -> "Network":
        """
        This function finds a network based on its unique id.

        :param id: Unique network id to search for.
        :return: A network based on a id.
        """
        return Network.query.filter_by(id=id).first()

    @staticmethod
    def get_by_owner(owner: int) -> "Network":
        """
        This function finds a network based on an User id.

        :param id: Unique User id to search for assigned networks.
        :return: A list of networks based on the User id.
        """
        return Network.query.filter_by(id=id).first()
