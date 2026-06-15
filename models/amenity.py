from models.enums import AmenityType, AssistanceType


class Amenity:
    def __init__(self, amenity_id: str, type: AmenityType, price: float):
        self._amenityId = amenity_id
        self._type = type
        self._price = price


class AssistanceRequest:
    def __init__(self, request_id: str, type: AssistanceType, is_fulfilled: bool = False):
        self._requestId = request_id
        self._type = type
        self._isFulfilled = is_fulfilled
