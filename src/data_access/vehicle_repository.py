from .repository import *
from config import GetConfigs

class VehicleRepository(Repository):
    def __init__(self):
        super(VehicleRepository, self).__init__()
        configs = GetConfigs()
        host = configs['db']['host']
        user = configs['db']['user']
        password = configs['db']['password']
        database = configs['db']['vehicle_database']
        self.Connect(host, user, password, database)

    def GetSTDDetail(self, stdId):
         sql = "SELECT Description FROM Vehicle_OperationMaster WHERE OperationID = '" + stdId + "'"
         return self.ExecQuery(sql)