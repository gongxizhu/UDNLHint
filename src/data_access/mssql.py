import pymssql

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def GetConnecttion(self):
        if not self.db:
            raise NameError("No database info")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise NameError("Connect to database failed")
        return self.conn

    def ExecQuery(self, sql, conn):
        cur = conn.cursor()
        cur.execute(sql)
        resList = cur.fetchall()

        return resList

    def ExecNonQuery(self, sql, conn):
        cur = conn.cursor()
        cur.execute(sql)
        self.conn.commit()