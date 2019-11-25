import os
import pandas as pd
from data_access.order_repository import *
from preparation.prepare_data import Prepare
from preparation.process_rawdata import LoadData, FormatToFile, LoadChassisLineMatrix, CalculateConfidenceMarginByChassis

def get_order_text_data():
    order_connector = OrderRepository()
    # orders = order_connector.GetUDOrders()
    # orderlines = order_connector.GetUDOrderlines()
    # columns_order = ['Id', 'OrderId', 'Notes', 'VehicleType', 'ServiceTypeCode', 'ChassisNumber', 'ModelNumber', 'MakeCode']
    # columns_orderline = ['Id', 'OrderId', 'Description', 'OrderLineId', 'LineType', 'JobId']
    # df_orders = pd.DataFrame.from_records(orders, columns = columns_order)
    # df_orderlines = pd.DataFrame.from_records(orderlines, columns = columns_orderline)

    # dirname = os.path.dirname(os.path.realpath(__file__))
    # df_orders.to_excel(os.path.join(dirname, "orders.xlsx"))
    # df_orderlines.to_excel(os.path.join(dirname, "orderlines.xlsx"))
    # textline = order_connector.GetTextAmountLineWithText()
    # print(textline)
    # print(df_orders)
    # print(df_orderlines)
    columns_data = [
        'OrderId', 'Text', 'Parts', 'DATs', 'STDs', 'Straights', 'TextAmounts'
    ]
    print("Loading data from Order database...")
    data = order_connector.GetOrderTextData()
    print("%.2f lines are loaded." % len(data))
    df_data = pd.DataFrame.from_records(data, columns=columns_data)
    print("Writing data to data.xlsx...")
    dirname = os.path.dirname(os.path.realpath(__file__))
    df_data.to_excel(os.path.join(dirname, "data.xlsx"))
    print("Done.")

def create_train_dataset():
    get_order_text_data()
    LoadData()
    FormatToFile()
    Prepare()

if __name__ == "__main__":
    create_train_dataset()
