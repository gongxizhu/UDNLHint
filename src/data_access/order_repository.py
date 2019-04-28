from .repository import *
from config import *

class OrderRepository(Repository):
    def __init__(self):
        super(OrderRepository, self).__init__()
        configs = GetConfigs()
        host = configs['db']['host']
        user = configs['db']['user']
        password = configs['db']['password']
        database = configs['db']['database']
        self.Connect(host, user, password, database)

    def GetUDOrders(self):
        sql = "SELECT ActiveOrder.Id AS orderKey, \
            ActiveOrder.OrderId, \
            Notes, \
            VehicleType, \
            ServiceTypeCode, \
            ChassisNumber, \
            ModelNumber, \
            MakeCode \
            FROM Order_Order AS ActiveOrder \
            LEFT JOIN \
            Order_OrderVehicleDetails AS VehicleDetails \
            ON ActiveOrder.Id = VehicleDetails.Id \
            where ChassisNumber like 'CD%' \
            OR ChassisNumber like 'CG%' \
            OR ChassisNumber like 'JNCU%' \
            AND MakeCode = 'UD' \
            ORDER BY OrderId"
        return self.ExecQuery(sql)

    def GetUDOrderlines(self, orderIds=None):
        sql = "SELECT Id, \
            OrderId, \
            Description, \
            OrderLineId, \
            LineType, \
            JobId \
            FROM Order_OrderLine \
            WHERE LineType IN (1, 2, 3, 4, 7) \
            AND OrderId IN (\
                SELECT ActiveOrder.Id \
                FROM Order_Order AS ActiveOrder \
                LEFT JOIN \
                Order_OrderVehicleDetails AS VehicleDetails \
                ON ActiveOrder.Id = VehicleDetails.Id \
                where ChassisNumber like 'CD%' \
                OR ChassisNumber like 'CG%' \
                OR ChassisNumber like 'JNCU%' \
                AND MakeCode = 'UD' \
            ) ORDER BY OrderId"
        return self.ExecQuery(sql)

    def GetSeq2SeqInput(self):
        pass

    def GetSeq2SeqOutput(self):
        pass