from .repository import *
from config import GetConfigs

class PackageRepository(Repository):
    def __init__(self):
        super(PackageRepository, self).__init__()
        configs = GetConfigs()
        host = configs['db']['host']
        user = configs['db']['user']
        password = configs['db']['password']
        database = configs['db']['package_database']
        self.Connect(host, user, password, database)

    def GetDATDetail(self, datId):
         sql = "SELECT Description FROM Package_DAT WHERE DATId = '" + datId + "'"
         return self.ExecQuery(sql)