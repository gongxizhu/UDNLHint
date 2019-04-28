from .mssql import *

class Repository(object):

    def __init__(self):
        pass

    def __del__(self):
        if not self._conn:
            self._conn.close()
    
    def Connect(self, host, user, pwd, db):
        self._db = MSSQL(host, user, pwd, db)
        self._conn = self._db.GetConnecttion()

    def ExecQuery(self, sql):
        return self._db.ExecQuery(sql, self._conn)