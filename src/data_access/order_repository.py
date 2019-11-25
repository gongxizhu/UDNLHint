from .repository import *
from config import *

class OrderRepository(Repository):
    def __init__(self):
        super(OrderRepository, self).__init__()
        configs = GetConfigs()
        host = configs['db']['host']
        user = configs['db']['user']
        password = configs['db']['password']
        database = configs['db']['order_database']
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

    def GetPartLineWithText(self):
        # Part
        sql = "SELECT TOP 1 Description, PartNumber \
                FROM Order_OrderLineArchive as OrderLinesArchive \
                LEFT JOIN \
                Order_PartLineArchive as PartLinesArchive \
                ON \
                PartLinesArchive.Id = OrderLinesArchive.Id\
                WHERE \
                LineType = 1 -- (1, 2, 3, 4, 7) \
                AND OrderId in (\
                    SELECT TOP 1000 ArchiveOrder.Id \
                    FROM Order_OrderArchive as ArchiveOrder \
                    LEFT JOIN \
                    Order_OrderVehicleDetailsArchive as VehicleDetailsArchive \
                    ON ArchiveOrder.Id = VehicleDetailsArchive.Id \
                    WHERE \
                    ChassisNumber like 'CD%' \
                    OR ChassisNumber like 'CG%' \
                    OR ChassisNumber like 'JNCU%' \
                    AND MakeCode = 'UD' \
                    AND OrderType = 1 \
                    AND OrderId <11657012\
                    ORDER BY OrderId \
                ) \
                AND Description is not null \
                AND Description <> ''"

        return self.ExecQuery(sql)

    def GetDATLineWithText(self):
        sql = "SELECT OrderLinesArchive.Description as LineDesc \
                ,JobArchive.Description as JobDesc \
	            ,OrderLinesArchive.LineType \
	            ,DATId \
                FROM Order_OrderLineArchive as OrderLinesArchive \
                LEFT JOIN \
                Order_LaborItemArchive as LaborItemArchive \
                ON LaborItemArchive.Id = OrderLinesArchive.Id \
                LEFT JOIN \
                Order_JobArchive as JobArchive \
                ON OrderLinesArchive.OrderId = JobArchive.OrderId \
                AND OrderLinesArchive.JobId = JobArchive.Id \
                LEFT JOIN \
                Order_OrderArchive as OrderArchive \
                ON OrderLinesArchive.OrderId = OrderArchive.Id \
                WHERE OrderLinesArchive.LineType = 2 -- (1, 2, 3, 4, 7) \
                AND OrderLinesArchive.OrderId in (\
                    SELECT TOP 1000 ArchiveOrder.Id \
                    FROM Order_OrderArchive as ArchiveOrder \
                    LEFT JOIN \
                    Order_OrderVehicleDetailsArchive as VehicleDetailsArchive \
                    ON ArchiveOrder.Id = VehicleDetailsArchive.Id \
                    WHERE \
                    ChassisNumber like 'CD%' \
                    OR ChassisNumber like 'CG%' \
                    OR ChassisNumber like 'JNCU%' \
                    AND MakeCode = 'UD' \
                    AND OrderType = 1 \
                    AND OrderId < 11657012\
                    ORDER BY OrderId \
                ) \
                AND OrderLinesArchive.[Description] is not null \
                AND OrderLinesArchive.[Description] <> '' \
                ORDER BY OrderLinesArchive.OrderId"
        return self.ExecQuery(sql)

    def GetSDTLineWithText(self):
        sql = "SELECT OrderLinesArchive.Description as LineDesc \
                ,JobArchive.Description as JobDesc \
	            ,OrderLinesArchive.LineType \
	            ,LaborId \
                FROM Order_OrderLineArchive as OrderLinesArchive \
                LEFT JOIN \
                Order_LaborItemArchive as LaborItemArchive \
                ON LaborItemArchive.Id = OrderLinesArchive.Id \
                LEFT JOIN \
                Order_JobArchive as JobArchive \
                ON OrderLinesArchive.OrderId = JobArchive.OrderId \
                AND OrderLinesArchive.JobId = JobArchive.Id \
                LEFT JOIN \
                Order_OrderArchive as OrderArchive \
                ON OrderLinesArchive.OrderId = OrderArchive.Id \
                WHERE OrderLinesArchive.LineType = 3 -- (1, 2, 3, 4, 7) \
                AND OrderLinesArchive.OrderId in (\
                    SELECT TOP 1000 ArchiveOrder.Id \
                    FROM Order_OrderArchive as ArchiveOrder \
                    LEFT JOIN \
                    Order_OrderVehicleDetailsArchive as VehicleDetailsArchive \
                    ON ArchiveOrder.Id = VehicleDetailsArchive.Id \
                    WHERE \
                    ChassisNumber like 'CD%' \
                    OR ChassisNumber like 'CG%' \
                    OR ChassisNumber like 'JNCU%' \
                    AND MakeCode = 'UD' \
                    AND OrderType = 1 \
                    AND OrderId < 11657012\
                    ORDER BY OrderId \
                ) \
                AND OrderLinesArchive.[Description] is not null \
                AND OrderLinesArchive.[Description] <> '' \
                ORDER BY OrderLinesArchive.OrderId"
        return self.ExecQuery(sql)

    def GetStraightLineWithText(self):
        sql = "SELECT OrderLinesArchive.Description as LineDesc \
                ,JobArchive.Description as JobDesc \
	            ,OrderLinesArchive.LineType \
                FROM Order_OrderLineArchive as OrderLinesArchive \
                LEFT JOIN \
                Order_LaborItemArchive as LaborItemArchive \
                ON LaborItemArchive.Id = OrderLinesArchive.Id \
                LEFT JOIN \
                Order_JobArchive as JobArchive \
                ON OrderLinesArchive.OrderId = JobArchive.OrderId \
                AND OrderLinesArchive.JobId = JobArchive.Id \
                LEFT JOIN \
                Order_OrderArchive as OrderArchive \
                ON OrderLinesArchive.OrderId = OrderArchive.Id \
                WHERE OrderLinesArchive.LineType = 4 -- (1, 2, 3, 4, 7) \
                AND OrderLinesArchive.OrderId in (\
                    SELECT TOP 1000 ArchiveOrder.Id \
                    FROM Order_OrderArchive as ArchiveOrder \
                    LEFT JOIN \
                    Order_OrderVehicleDetailsArchive as VehicleDetailsArchive \
                    ON ArchiveOrder.Id = VehicleDetailsArchive.Id \
                    WHERE \
                    ChassisNumber like 'CD%' \
                    OR ChassisNumber like 'CG%' \
                    OR ChassisNumber like 'JNCU%' \
                    AND MakeCode = 'UD' \
                    AND OrderType = 1 \
                    AND OrderId < 11657012\
                    ORDER BY OrderId \
                ) \
                AND OrderLinesArchive.[Description] is not null \
                AND OrderLinesArchive.[Description] <> '' \
                ORDER BY OrderLinesArchive.OrderId"
        return self.ExecQuery(sql)


    def GetTextAmountLineWithText(self):
        sql = "SELECT top 10 OrderLinesArchive.Description as LineDesc \
                ,JobArchive.Description as JobDesc \
	            ,OrderLinesArchive.LineType \
                FROM Order_OrderLineArchive as OrderLinesArchive \
                LEFT JOIN \
                Order_TextAmountLineArchive as TextAmountLineArchive \
                ON TextAmountLineArchive.Id = OrderLinesArchive.Id \
                LEFT JOIN \
                Order_JobArchive as JobArchive \
                ON OrderLinesArchive.OrderId = JobArchive.OrderId \
                AND OrderLinesArchive.JobId = JobArchive.Id \
                LEFT JOIN \
                Order_OrderArchive as OrderArchive \
                ON OrderLinesArchive.OrderId = OrderArchive.Id \
                WHERE OrderLinesArchive.LineType = 7 -- (1, 2, 3, 4, 7) \
                AND OrderLinesArchive.OrderId in (\
                    SELECT TOP 1000 ArchiveOrder.Id \
                    FROM Order_OrderArchive as ArchiveOrder \
                    LEFT JOIN \
                    Order_OrderVehicleDetailsArchive as VehicleDetailsArchive \
                    ON ArchiveOrder.Id = VehicleDetailsArchive.Id \
                    WHERE \
                    ChassisNumber like 'CD%' \
                    OR ChassisNumber like 'CG%' \
                    OR ChassisNumber like 'JNCU%' \
                    AND MakeCode = 'UD' \
                    AND OrderType = 1 \
                    AND OrderId < 11657012\
                    ORDER BY OrderId \
                ) \
                AND OrderLinesArchive.[Description] is not null \
                AND OrderLinesArchive.[Description] <> '' \
                ORDER BY OrderLinesArchive.OrderId"
        return self.ExecQuery(sql)

    def GetOrderTextData(self):
        sql='SELECT Id as OrderId \
            ,Text=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Notes \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Id = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
                + \',\' + STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Description \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
                + \',\' + STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].Description \
                    FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].OrderId = SelectedOrders.Id \
                    AND [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].LineType in (2, 3, 4, 7) \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,Parts=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.PartNumber \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,DATs=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.DATId \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,STDs=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.LaborId \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,Straights=( \
                    SELECT COUNT(*) \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    AND LineType = 4 \
                ) \
            ,TextAmmounts=( \
                    SELECT COUNT(*) \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    AND LineType = 7 \
                ) \
            FROM \
            (\
                SELECT DISTINCT TOP 20000 OrderArchive.Id as Id \
                FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive \
                LEFT JOIN \
                [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive \
                ON OrderArchive.Id = OrderLinesArchive.OrderId \
                LEFT JOIN \
                [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive \
                ON OrderArchive.Id = VehicleDetailsArchive.Id \
                WHERE ChassisNumber like \'CD%\' \
                    OR ChassisNumber like \'CG%\' \
                    OR ChassisNumber like \'JNCU%\' \
                    AND MakeCode = \'UD\' \
                    AND OrderType = 1 \
                    AND OrderArchive.Id < 11657012 \
                    AND OrderLinesArchive.LineType in (2, 3, 4, 7) \
                ORDER BY OrderArchive.Id \
            ) AS SelectedOrders \
            GROUP BY SelectedOrders.Id \
            ORDER BY SelectedOrders.Id'
        # print(sql)
        return self.ExecQuery(sql)
    
    def GetOrderChassisMapping(self):
        sql='SELECT SelectedOrders.Id as OrderId \
            ,MAX(VehicleDetailsArchive.ChassisNumber) as ChassisNumber \
            ,Parts=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.PartNumber \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,DATs=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.DATId \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,STDs=STUFF(( \
                    SELECT \',\' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.LaborId \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive \
                    LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    FOR XML PATH(\'\'), TYPE).value(\'.\', \'NVARCHAR(MAX)\'), \
                1, 1, \'\') \
            ,Straights=( \
                    SELECT COUNT(*) \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    AND LineType = 4 \
                ) \
            ,TextAmmounts=( \
                    SELECT COUNT(*) \
                    FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive \
                    WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id \
                    AND LineType = 7 \
                ) \
            FROM \
            (\
                SELECT DISTINCT TOP 20000 OrderArchive.Id as Id \
                FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive \
                LEFT JOIN \
                [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive \
                ON OrderArchive.Id = OrderLinesArchive.OrderId \
                LEFT JOIN \
                [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive \
                ON OrderArchive.Id = VehicleDetailsArchive.Id \
                WHERE ChassisNumber like \'CD%\' \
                    OR ChassisNumber like \'CG%\' \
                    OR ChassisNumber like \'JNCU%\' \
                    AND MakeCode = \'UD\' \
                    AND OrderType = 1 \
                    AND OrderArchive.Id < 11657012 \
                    AND OrderLinesArchive.LineType in (2, 3, 4, 7) \
                ORDER BY OrderArchive.Id \
            ) AS SelectedOrders \
            LEFT JOIN \
            [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive \
            ON VehicleDetailsArchive.Id = SelectedOrders.Id \
            GROUP BY SelectedOrders.Id \
            ORDER BY SelectedOrders.Id'
        # print(sql)
        return self.ExecQuery(sql)

    def GetDATDetail(self, datId):
        pass