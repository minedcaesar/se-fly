from abc import ABC, abstractmethod


class OAuthProvider(ABC):
    @abstractmethod
    def authenticateUser(self, auth_code):
        pass
    @abstractmethod
    def fetchBasicProfile(self, access_token):
        pass


class WeatherForecastAPI(ABC):

    @abstractmethod
    def getWeeklyForecast(self):
        pass


class PaymentProvider(ABC):
    @abstractmethod
    def processTransaction(self, item_id, amount, reference):
        pass


class TicketPlatform(ABC):
    @abstractmethod
    def handleBookingRedirection(self, flight_id, origin, destination):
        pass


class CityServiceProvider(ABC):
    @abstractmethod
    def handleServiceRedirection(self, service_id):
        pass


class AirTrafficControl(ABC):
    @abstractmethod
    def provideFlightData(self):
        pass