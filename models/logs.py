from abc import ABC
from datetime import datetime


class SystemLogEntry(ABC):
    def __init__(self, log_entry_id: str, timestamp: datetime):
        self._logEntryId = log_entry_id
        self._timestamp = timestamp


class AuditLogEntry(SystemLogEntry):
    def __init__(self, log_entry_id: str, timestamp: datetime,
                 user_id: int, flight_id: str, action_performed: str):
        super().__init__(log_entry_id, timestamp)
        self._userId = user_id
        self._flightId = flight_id
        self._actionPerformed = action_performed


class AccountabilityLogEntry(SystemLogEntry):
    def __init__(self, log_entry_id: str, timestamp: datetime,
                 manager_id: int, staff_id: int, reason_for_change: str):
        super().__init__(log_entry_id, timestamp)
        self._managerId = manager_id
        self._staffId = staff_id
        self._reasonForChange = reason_for_change