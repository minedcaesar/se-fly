from abc import ABC, abstractmethod
from datetime import date, datetime
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


class Staff(User, ABC):
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, assigned_department: str):
        super().__init__(user_id)
        self._employeeId = employee_id
        self._fullName = full_name
        self._email = email
        self._assignedDepartment = assigned_department

    @abstractmethod
    def accessDashboard(self):
        pass


class AirlineStaff(Staff, ABC):
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, department: str, airline_name: str):
        super().__init__(user_id, employee_id, full_name, email, department)
        self._airlineName = airline_name

    def viewFlightSchedules(self):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


class AirlineScheduleStaff(AirlineStaff):
    def addFlightSchedule(self, schedule_data=None):
        raise NotImplementedError

    def deleteFlightSchedule(self, flight_number=None):
        raise NotImplementedError

    def editFlightSchedule(self, flight_number=None, updates=None):
        raise NotImplementedError

    def submitFlightInformation(self, instance_id=None, info=None):
        raise NotImplementedError


class AirlineManager(AirlineStaff):
    def accessAuditLogs(self):
        raise NotImplementedError


class GroundStaff(Staff, ABC):
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, department: str, assigned_terminal: str):
        super().__init__(user_id, employee_id, full_name, email, department)
        self._assignedTerminal = assigned_terminal

    def monitorGroundOperations(self):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


class GroundOperationManager(GroundStaff):
    def moveAircraft(self, aircraft_id=None, target_gate=None):
        raise NotImplementedError

    def reassignResources(self, resource_id=None, task_id=None):
        raise NotImplementedError

    def createOperationPlan(self, flight_instance_id=None):
        raise NotImplementedError


class ShiftScheduleManager(GroundStaff):
    def communicateShifts(self, shift_data=None):
        raise NotImplementedError

    def assignShift(self, staff_id=None, shift_id=None):
        raise NotImplementedError


class OperationStaff(GroundStaff):
    def viewAssignedTasks(self):
        raise NotImplementedError


class SystemAdmin(Staff):
    def createStaffAccount(self, staff_data=None):
        raise NotImplementedError

    def deleteStaffAccount(self, user_id=None):
        raise NotImplementedError

    def assignRoles(self, user_id=None, new_role=None):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


class Session:
    def __init__(self, session_id: str, device_id: str,
                 login_timestamp: datetime, is_active: bool = True):
        self._sessionId = session_id
        self._deviceId = device_id
        self._loginTimestamp = login_timestamp
        self._isActive = is_active

    def terminate(self):
        raise NotImplementedError


class Shift:
    def __init__(self, shift_id: str, start_time: datetime, end_time: datetime):
        self._shiftId = shift_id
        self._startTime = start_time
        self._endTime = end_time
