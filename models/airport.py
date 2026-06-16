## @file airport.py
#  @brief Airport infrastructure and autonomous systems.


## @brief Static and dynamic airport information shown to clients.
class AirportInformation:

    ## @brief Build the airport information record.
    #  @param map_data         Map of the airport (SVG/string).
    #  @param parking_avail    Number of free parking spaces.
    #  @param regulations_text Passenger regulations text.
    #  @param city_context     Surrounding-city information.
    def __init__(self, map_data="", parking_avail=0, regulations_text="", city_context=""):
        self._mapData = map_data
        self._parkingAvailability = parking_avail
        self._regulationsText = regulations_text
        self._cityContextInfo = city_context

    ## @brief Return the airport map.
    #  @return map data.
    def getMap(self):
        raise NotImplementedError

    ## @brief Return current parking availability.
    #  @return number of free spaces.
    def getParkingInfo(self):
        raise NotImplementedError


## @brief Coordinates the airport's response to an emergency.
class EmergencySystem:

    ## @brief Build the emergency system.
    #  @param allocator     Resource allocator to drive.
    #  @param backup_server Backup server to fail over to.
    def __init__(self, allocator, backup_server):
        self._allocator = allocator
        self._backupServer = backup_server

    ## @brief Put the airport into emergency mode (UC23).
    def implementEmergencyProtocols(self):
        raise NotImplementedError

    ## @brief Take over operations on the backup server.
    def takeoverFunctions(self):
        raise NotImplementedError


## @brief Generates baseline operation plans automatically.
class AutomaticResourceAllocator:

    ## @brief Generate a default plan for a flight instance.
    #  @param flight_instance_id  Target flight instance.
    def generateBaselinePlan(self, flight_instance_id=None):
        raise NotImplementedError

    ## @brief Check resource availability for a plan.
    #  @param plan_id  Plan to check.
    def performAvailabilityCheck(self, plan_id=None):
        raise NotImplementedError


## @brief A sensor reporting an aircraft's position on the ground.
class AirportSensor:

    ## @brief Build a sensor.
    #  @param sensor_id  Unique identifier.
    #  @param location   Physical location.
    def __init__(self, sensor_id: str, location: str):
        self._sensorId = sensor_id
        self._location = location

    ## @brief Broadcast the tracked aircraft's position.
    def broadcastAircraftPosition(self):
        raise NotImplementedError


## @brief Standby server that can take over primary operations.
class BackupServer:

    ## @brief Build the backup server.
    #  @param is_standby  Whether it is currently on standby.
    def __init__(self, is_standby: bool = True):
        self._isStandby = is_standby

    ## @brief Promote this server to primary.
    def assumePrimaryOperations(self):
        raise NotImplementedError