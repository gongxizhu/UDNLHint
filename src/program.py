import pandas as pd
import os
from data_access.order_repository import *

def main():
    order_connector = OrderRepository()
    orders = order_connector.GetUDOrders()
    orderlines = order_connector.GetUDOrderlines()
    columns_order = ['Id', 'OrderId', 'Notes', 'VehicleType', 'ServiceTypeCode', 'ChassisNumber', 'ModelNumber', 'MakeCode']
    columns_orderline = ['Id', 'OrderId', 'Description', 'OrderLineId', 'LineType', 'JobId']
    df_orders = pd.DataFrame.from_records(orders, columns = columns_order)
    df_orderlines = pd.DataFrame.from_records(orderlines, columns = columns_orderline)
    
    dirname = os.path.dirname(os.path.realpath(__file__))
    df_orders.to_excel(os.path.join(dirname, "orders.xlsx"))
    df_orderlines.to_excel(os.path.join(dirname, "orderlines.xlsx"))
    # print(df_orders)
    # print(df_orderlines)
 
if __name__ == "__main__":
    main()