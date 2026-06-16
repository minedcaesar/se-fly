## @file external.py
#  @brief Interfaces to external systems. The real calls are written but commented out,
#         with a mock used for the deliverable (D3 rule: external connections present but disabled).

from abc import ABC, abstractmethod


## @brief OAuth provider used to authenticate clients (e.g. Google).
class OAuthProvider(ABC):

    ## @brief Exchange an authorisation code for an access token.
    #  @param auth_code  Code returned by the provider's consent screen.
    #  @return token payload (mocked in this deliverable).
    # production:
    #   token = requests.post("https://oauth2.googleapis.com/token", data={...}).json()
    @abstractmethod
    def authenticateUser(self, auth_code):
        pass

    ## @brief Fetch the authenticated user's basic profile.
    #  @param access_token  OAuth access token.
    #  @return profile dict with email and name (mocked).
    # production:
    #   requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
    #       headers={"Authorization": f"Bearer {access_token}"})
    @abstractmethod
    def fetchBasicProfile(self, access_token):
        pass


## @brief Weather feed used by ground staff (OpenWeatherMap).
class WeatherForecastAPI(ABC):

    ## @brief Get the multi-day forecast for the airport location.
    #  @return list of daily forecasts (mocked).
    # production:
    #   requests.get("https://api.openweathermap.org/data/2.5/forecast", params={...})
    @abstractmethod
    def getWeeklyForecast(self):
        pass


## @brief Payment provider used when a client buys an amenity.
class PaymentProvider(ABC):

    ## @brief Start a hosted-checkout transaction.
    #  @param item_id    Amenity being purchased.
    #  @param amount     Amount in EUR.
    #  @param reference  Internal transaction reference.
    #  @return redirect URL to the checkout page (mocked).
    @abstractmethod
    def processTransaction(self, item_id, amount, reference):
        pass


## @brief External airline ticketing platform clients are redirected to.
class TicketPlatform(ABC):

    ## @brief Build a booking redirection for a flight.
    @abstractmethod
    def handleBookingRedirection(self, flight_id, origin, destination):
        pass


## @brief External city-service provider (transport, hotels, ...).
class CityServiceProvider(ABC):

    ## @brief Redirect the client to a city service.
    @abstractmethod
    def handleServiceRedirection(self, service_id):
        pass


## @brief Air-traffic-control feed providing live flight data.
class AirTrafficControl(ABC):

    ## @brief Pull current flight data from the feed.
    #  @return list of flight states (mocked).
    # production:
    #   requests.get(ATC_API_URL, headers={"Authorization": f"Bearer {ATC_TOKEN}"})
    @abstractmethod
    def provideFlightData(self):
        pass