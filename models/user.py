from abc import ABC, abstractmethod
from datetime import date
from typing import List


class User(ABC):
    def __init__(self, user_id: int):
        self._userId = user_id
        self._sessions: List = []


class Client(User, ABC):
    @abstractmethod
    def browseFlights(self):
        pass

    @abstractmethod
    def viewAirportInfo(self):
        pass


class UnregisteredClient(Client):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def createAccount(self):
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def browseFlights(self):
        raise NotImplementedError

    def viewAirportInfo(self):
        raise NotImplementedError


class RegisteredClient(Client):
    def __init__(self, user_id: int, full_name: str, email: str,
                 dob: date, oauth_token: str):
        super().__init__(user_id)
        self._fullName = full_name
        self._email = email
        self._dateOfBirth = dob
        self._oauthToken = oauth_token

    def manageProfile(self):
        raise NotImplementedError

    def purchaseAmenities(self, amenity_id=None):
        raise NotImplementedError

    def requestAssistance(self, assistance_type=None, flight_number=None):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def deleteAccount(self):
        raise NotImplementedError

    def browseFlights(self):
        raise NotImplementedError

    def viewAirportInfo(self):
        raise NotImplementedError
