class AirportInformation:
    def __init__(self, map_data="", parking_avail=0, regulations_text="", city_context=""):
        self._mapData = map_data
        self._parkingAvailability = parking_avail
        self._regulationsText = regulations_text
        self._cityContextInfo = city_context

    def getMap(self):
        raise NotImplementedError

    def getParkingInfo(self):
        raise NotImplementedError


class EmergencySystem:
    def __init__(self, allocator, backup_server):
        self._allocator = allocator
        self._backupServer = backup_server

    def implementEmergencyProtocols(self):
        raise NotImplementedError

    def takeoverFunctions(self):
        raise NotImplementedError


class AutomaticResourceAllocator:
    def generateBaselinePlan(self, flight_instance_id=None):
        raise NotImplementedError

    def performAvailabilityCheck(self, plan_id=None):
        raise NotImplementedError


class AirportSensor:
    def __init__(self, sensor_id: str, location: str):
        self._sensorId = sensor_id
        self._location = location

    def broadcastAircraftPosition(self):
        raise NotImplementedError


class BackupServer:
    def __init__(self, is_standby: bool = True):
        self._isStandby = is_standby

    def assumePrimaryOperations(self):
        raise NotImplementedError
