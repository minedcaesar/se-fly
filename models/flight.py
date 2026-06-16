## @file flight.py
#  @brief Flight domain models: Airline, FlightSchedule, FlightInstance, Aircraft, Gate, Terminal.
#  A FlightSchedule is a recurring template; it generates FlightInstance occurrences.

from datetime import datetime
from typing import Optional
from models.enums import FlightStatus


## @brief An airline operating at the airport.
class Airline:

    ## @brief Build an airline.
    #  @param airline_id  Unique identifier.
    #  @param name        Airline name.
    #  @param country     Country of registration.
    def __init__(self, airline_id: int, name: str, country: str):
        self._airlineId = airline_id
        self._name = name
        self._country = country


## @brief A recurring flight schedule (the template instances are generated from).
class FlightSchedule:

    ## @brief Build a schedule.
    #  @param flight_number   IATA flight number.
    #  @param origin          Origin IATA code.
    #  @param destination     Destination IATA code.
    #  @param recurrence_rule Recurrence, e.g. "DAILY".
    def __init__(self, flight_number: str, origin: str,
                 destination: str, recurrence_rule: str):
        self._flightNumber = flight_number
        self._origin = origin
        self._destination = destination
        self._recurrenceRule = recurrence_rule

    ## @brief Update the schedule's status.
    #  @param new_status  New status value.
    def updateStatus(self, new_status=None):
        raise NotImplementedError

    ## @brief Assign a gate to the schedule.
    #  @param gate_id  Gate to assign.
    def assignGate(self, gate_id=None):
        raise NotImplementedError


## @brief One dated occurrence of a FlightSchedule.
class FlightInstance:

    ## @brief Build a flight instance.
    #  @param instance_id               Unique identifier.
    #  @param scheduled_departure_time  Planned departure time.
    #  @param scheduled_arrival_time    Planned arrival time.
    #  @param status                    Initial FlightStatus.
    def __init__(self, instance_id: str,
                 scheduled_departure_time: datetime,
                 scheduled_arrival_time: datetime,
                 status: FlightStatus = FlightStatus.SCHEDULED):
        self._instanceId = instance_id
        self._scheduledDepartureTime = scheduled_departure_time
        self._scheduledArrivalTime = scheduled_arrival_time
        self._actualDepartureTime: Optional[datetime] = None
        self._actualArrivalTime: Optional[datetime] = None
        self._status = status

    ## @brief Update the instance status.
    #  @param new_status  New FlightStatus.
    def updateStatus(self, new_status: FlightStatus = None):
        raise NotImplementedError


## @brief A physical aircraft.
class Aircraft:

    ## @brief Build an aircraft.
    #  @param aircraft_id      Unique identifier / registration.
    #  @param model            Aircraft model.
    #  @param capacity         Seat capacity.
    #  @param current_status   Operational status.
    #  @param current_position Current gate or stand.
    def __init__(self, aircraft_id: str, model: str, capacity: int,
                 current_status: str, current_position: str):
        self._aircraftId = aircraft_id
        self._model = model
        self._capacity = capacity
        self._currentStatus = current_status
        self._currentPosition = current_position


## @brief A boarding gate.
class Gate:

    ## @brief Build a gate.
    #  @param gate_id       Unique identifier.
    #  @param is_available  Whether the gate is free.
    def __init__(self, gate_id: str, is_available: bool = True):
        self._gateId = gate_id
        self._isAvailable = is_available

    ## @brief Park an aircraft at this gate.
    #  @param aircraft_id  Aircraft to park.
    def assignAircraft(self, aircraft_id=None):
        raise NotImplementedError

    ## @brief Free the gate.
    def releaseGate(self):
        raise NotImplementedError


## @brief A terminal building.
class Terminal:

    ## @brief Build a terminal.
    #  @param terminal_id  Unique identifier.
    #  @param name         Display name.
    def __init__(self, terminal_id: str, name: str):
        self._terminalId = terminal_id
        self._name = name