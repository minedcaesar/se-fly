## @file enums.py
#  @brief Enumeration types used across the FLY domain model.
#  The string values are the exact literals stored in the database.

from enum import Enum


## @brief Lifecycle status of a flight instance.
class FlightStatus(Enum):
    SCHEDULED = "Scheduled"
    BOARDING = "Boarding"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"
    DEPARTED = "Departed"
    ARRIVED = "Arrived"


## @brief State of a ground operation plan.
class PlanStatus(Enum):
    DRAFT = "Draft"
    SAVED = "Saved"


## @brief Status of a ground task.
class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    DELAYED = "Delayed"


## @brief Type of purchasable airport amenity.
class AmenityType(Enum):
    LINE_SKIP = "LineSkip"
    FAST_TRACK = "FastTrack"
    LOUNGE_ACCESS = "LoungeAccess"


## @brief Type of special-assistance a client can request.
class AssistanceType(Enum):
    WHEELCHAIR_SERVICE = "WheelchairService"
    PRIORITY_BOARDING = "PriorityBoarding"
    UNACCOMPANIED_MINOR = "UnaccompaniedMinor"