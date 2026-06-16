## @file logs.py
#  @brief Audit and accountability log models. Log entries are immutable once written.

from abc import ABC
from datetime import datetime


## @brief Base class for all system log entries.
class SystemLogEntry(ABC):

    ## @brief Build a log entry.
    #  @param log_entry_id  Unique identifier of the entry.
    #  @param timestamp     When the logged event happened.
    def __init__(self, log_entry_id: str, timestamp: datetime):
        self._logEntryId = log_entry_id
        self._timestamp = timestamp


## @brief Records a change to a flight schedule (add / remove).
class AuditLogEntry(SystemLogEntry):

    ## @brief Build an audit entry.
    #  @param log_entry_id     Unique identifier of the entry.
    #  @param timestamp        When the logged event happened.
    #  @param user_id          Staff member who performed the action.
    #  @param flight_id        Flight number affected.
    #  @param action_performed Action, e.g. "ADDED" or "DELETED".
    def __init__(self, log_entry_id: str, timestamp: datetime,
                 user_id: int, flight_id: str, action_performed: str):
        super().__init__(log_entry_id, timestamp)
        self._userId = user_id
        self._flightId = flight_id
        self._actionPerformed = action_performed


## @brief Records a managerial decision affecting staff or aircraft.
class AccountabilityLogEntry(SystemLogEntry):

    ## @brief Build an accountability entry.
    #  @param log_entry_id      Unique identifier of the entry.
    #  @param timestamp         When the logged event happened.
    #  @param manager_id        Manager responsible for the decision.
    #  @param staff_id          Staff member affected.
    #  @param reason_for_change Justification text.
    def __init__(self, log_entry_id: str, timestamp: datetime,
                 manager_id: int, staff_id: int, reason_for_change: str):
        super().__init__(log_entry_id, timestamp)
        self._managerId = manager_id
        self._staffId = staff_id
        self._reasonForChange = reason_for_change