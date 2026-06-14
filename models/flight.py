from datetime import datetime
from typing import Optional
from models.enums import FlightStatus


class Airline:
    def __init__(self, airline_id: int, name: str, country: str):
        self._airlineId = airline_id
        self._name = name
        self._country = country


class FlightSchedule:
    def __init__(self, flight_number: str, origin: str,
                 destination: str, recurrence_rule: str):
        self._flightNumber = flight_number
        self._origin = origin
        self._destination = destination
        self._recurrenceRule = recurrence_rule

    def updateStatus(self, new_status=None):
        raise NotImplementedError

    def assignGate(self, gate_id=None):
        raise NotImplementedError


class FlightInstance:
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

    def updateStatus(self, new_status: FlightStatus = None):
        raise NotImplementedError


class Aircraft:
    def __init__(self, aircraft_id: str, model: str, capacity: int,
                 current_status: str, current_position: str):
        self._aircraftId = aircraft_id
        self._model = model
        self._capacity = capacity
        self._currentStatus = current_status
        self._currentPosition = current_position


class Gate:
    def __init__(self, gate_id: str, is_available: bool = True):
        self._gateId = gate_id
        self._isAvailable = is_available

    def assignAircraft(self, aircraft_id=None):
        raise NotImplementedError

    def releaseGate(self):
        raise NotImplementedError


class Terminal:
    def __init__(self, terminal_id: str, name: str):
        self._terminalId = terminal_id
        self._name = name