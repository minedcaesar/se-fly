## @file amenity.py
#  @brief Purchasable amenities and special-assistance requests.

from models.enums import AmenityType, AssistanceType


## @brief An amenity a client can purchase (fast track, lounge access, ...).
class Amenity:

    ## @brief Build an amenity.
    #  @param amenity_id  Unique identifier.
    #  @param type        AmenityType value.
    #  @param price       Price in EUR.
    def __init__(self, amenity_id: str, type: AmenityType, price: float):
        self._amenityId = amenity_id
        self._type = type
        self._price = price


## @brief A client's request for special assistance on a flight.
class AssistanceRequest:

    ## @brief Build an assistance request.
    #  @param request_id    Unique identifier.
    #  @param type          AssistanceType value.
    #  @param is_fulfilled  Whether the request has been handled.
    def __init__(self, request_id: str, type: AssistanceType, is_fulfilled: bool = False):
        self._requestId = request_id
        self._type = type
        self._isFulfilled = is_fulfilled