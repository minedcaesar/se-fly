## @file user.py
#  @brief User domain model (mirrors the D2 class diagram).
#    User -> Client -> UnregisteredClient / RegisteredClient
#    User -> Staff  -> AirlineStaff -> AirlineScheduleStaff / AirlineManager
#                   -> GroundStaff  -> GroundOperationManager / ShiftScheduleManager / OperationStaff
#                   -> SystemAdmin
#  Session and Shift also hang off the user side of the model.

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List


## @brief Base class for everyone who interacts with the system.
class User(ABC):

    ## @brief Build a user.
    #  @param user_id  Unique identifier.
    def __init__(self, user_id: int):
        self._userId = user_id
        self._sessions: List = []


# --- Client branch ---

## @brief A client of the airport (registered or not).
class Client(User, ABC):

    ## @brief Browse the public flight board.
    @abstractmethod
    def browseFlights(self):
        pass

    ## @brief View public airport information.
    @abstractmethod
    def viewAirportInfo(self):
        pass


## @brief A visitor who has not logged in.
class UnregisteredClient(Client):

    ## @brief Build an unregistered client. @param user_id id.
    def __init__(self, user_id: int):
        super().__init__(user_id)

    ## @brief Create an account (UC01).
    def createAccount(self):
        raise NotImplementedError

    ## @brief Log in via OAuth (UC02).
    def login(self):
        raise NotImplementedError

    def browseFlights(self):
        raise NotImplementedError

    def viewAirportInfo(self):
        raise NotImplementedError


## @brief A logged-in client.
class RegisteredClient(Client):

    ## @brief Build a registered client.
    #  @param user_id     Unique identifier.
    #  @param full_name   Full name.
    #  @param email       Email address.
    #  @param dob         Date of birth.
    #  @param oauth_token OAuth token from the provider.
    def __init__(self, user_id: int, full_name: str, email: str,
                 dob: date, oauth_token: str):
        super().__init__(user_id)
        self._fullName = full_name
        self._email = email
        self._dateOfBirth = dob
        self._oauthToken = oauth_token

    ## @brief Edit profile information (UC07).
    def manageProfile(self):
        raise NotImplementedError

    ## @brief Purchase an amenity (UC05). @param amenity_id amenity.
    def purchaseAmenities(self, amenity_id=None):
        raise NotImplementedError

    ## @brief Request special assistance (UC06).
    #  @param assistance_type  AssistanceType.
    #  @param flight_number    Related flight.
    def requestAssistance(self, assistance_type=None, flight_number=None):
        raise NotImplementedError

    ## @brief Log out (UC07/UC02).
    def logout(self):
        raise NotImplementedError

    ## @brief Delete (anonymise) the account (UC08).
    def deleteAccount(self):
        raise NotImplementedError

    def browseFlights(self):
        raise NotImplementedError

    def viewAirportInfo(self):
        raise NotImplementedError


# --- Staff branch ---

## @brief Base class for internal staff (login with email + password).
class Staff(User, ABC):

    ## @brief Build a staff member.
    #  @param user_id             Unique identifier.
    #  @param employee_id         Employee number (distinct from user_id).
    #  @param full_name           Full name.
    #  @param email               Work email.
    #  @param assigned_department Department.
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, assigned_department: str):
        super().__init__(user_id)
        self._employeeId = employee_id
        self._fullName = full_name
        self._email = email
        self._assignedDepartment = assigned_department

    ## @brief Open the role-specific dashboard.
    @abstractmethod
    def accessDashboard(self):
        pass


## @brief Staff employed by an airline.
class AirlineStaff(Staff, ABC):

    ## @brief Build an airline staff member.
    #  @param airline_name  Airline they work for.
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, department: str, airline_name: str):
        super().__init__(user_id, employee_id, full_name, email, department)
        self._airlineName = airline_name

    ## @brief View the airline's flight schedules (UC09).
    def viewFlightSchedules(self):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


## @brief Airline staff who edit schedules (UC10/UC11).
class AirlineScheduleStaff(AirlineStaff):

    ## @brief Add a flight schedule (UC10). @param schedule_data fields.
    def addFlightSchedule(self, schedule_data=None):
        raise NotImplementedError

    ## @brief Remove a flight schedule (UC11). @param flight_number flight.
    def deleteFlightSchedule(self, flight_number=None):
        raise NotImplementedError

    ## @brief Edit a flight schedule. @param flight_number flight. @param updates fields.
    def editFlightSchedule(self, flight_number=None, updates=None):
        raise NotImplementedError

    ## @brief Submit live flight information. @param instance_id instance. @param info data.
    def submitFlightInformation(self, instance_id=None, info=None):
        raise NotImplementedError


## @brief Airline manager with access to schedule logs (UC12).
class AirlineManager(AirlineStaff):

    ## @brief Read the airline's audit log (UC12).
    def accessAuditLogs(self):
        raise NotImplementedError


## @brief Base class for ground staff.
class GroundStaff(Staff, ABC):

    ## @brief Build a ground staff member.
    #  @param assigned_terminal  Terminal they work in.
    def __init__(self, user_id: int, employee_id: int, full_name: str,
                 email: str, department: str, assigned_terminal: str):
        super().__init__(user_id, employee_id, full_name, email, department)
        self._assignedTerminal = assigned_terminal

    ## @brief Monitor the ground environment (UC15).
    def monitorGroundOperations(self):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


## @brief Ground manager who can move aircraft and resources (UC16/UC17/UC18).
class GroundOperationManager(GroundStaff):

    ## @brief Move an aircraft to a new gate (UC16).
    #  @param aircraft_id  Aircraft to move.
    #  @param target_gate  Destination gate.
    def moveAircraft(self, aircraft_id=None, target_gate=None):
        raise NotImplementedError

    ## @brief Reassign a resource to a task (UC17).
    def reassignResources(self, resource_id=None, task_id=None):
        raise NotImplementedError

    ## @brief Create an operation plan (UC18). @param flight_instance_id instance.
    def createOperationPlan(self, flight_instance_id=None):
        raise NotImplementedError


## @brief Manager who publishes shifts (UC19).
class ShiftScheduleManager(GroundStaff):

    ## @brief Publish shifts to staff (UC19). @param shift_data shifts.
    def communicateShifts(self, shift_data=None):
        raise NotImplementedError

    ## @brief Assign a shift to a staff member. @param staff_id staff. @param shift_id shift.
    def assignShift(self, staff_id=None, shift_id=None):
        raise NotImplementedError


## @brief Operation staff who carry out tasks (UC20/UC14).
class OperationStaff(GroundStaff):

    ## @brief View the tasks assigned to this staff member.
    def viewAssignedTasks(self):
        raise NotImplementedError


## @brief System administrator who manages staff accounts (UC21/UC22).
class SystemAdmin(Staff):

    ## @brief Create a staff account (UC21). @param staff_data fields.
    def createStaffAccount(self, staff_data=None):
        raise NotImplementedError

    ## @brief Delete a staff account (UC22). @param user_id account.
    def deleteStaffAccount(self, user_id=None):
        raise NotImplementedError

    ## @brief Change a staff member's role. @param user_id account. @param new_role role.
    def assignRoles(self, user_id=None, new_role=None):
        raise NotImplementedError

    def accessDashboard(self):
        raise NotImplementedError


# --- Session / Shift ---

## @brief An authenticated session. Only one is active per user (NF16).
class Session:

    ## @brief Build a session.
    #  @param session_id      Unique identifier.
    #  @param device_id       Device / user-agent.
    #  @param login_timestamp When the session started.
    #  @param is_active       Whether it is the active session.
    def __init__(self, session_id: str, device_id: str,
                 login_timestamp: datetime, is_active: bool = True):
        self._sessionId = session_id
        self._deviceId = device_id
        self._loginTimestamp = login_timestamp
        self._isActive = is_active

    ## @brief Invalidate this session.
    def terminate(self):
        raise NotImplementedError


## @brief A work shift assigned to a staff member.
class Shift:

    ## @brief Build a shift.
    #  @param shift_id    Unique identifier.
    #  @param start_time  Shift start.
    #  @param end_time    Shift end.
    def __init__(self, shift_id: str, start_time: datetime, end_time: datetime):
        self._shiftId = shift_id
        self._startTime = start_time
        self._endTime = end_time