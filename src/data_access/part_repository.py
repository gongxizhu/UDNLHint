from .repository import *
from config import GetConfigs

class PartRepository(Repository):
    def __init__(self):
        super(PartRepository, self).__init__()
        configs = GetConfigs()
        host = configs['db']['host']
        user = configs['db']['user']
        password = configs['db']['password']
        database = configs['db']['part_database']
        self.Connect(host, user, password, database)

    def GetPartDetail(self, partnumber):
         sql = "SELECT PartDescription FROM Part_Part WHERE PartNumber = '" + partnumber + "'"
         return self.ExecQuery(sql)