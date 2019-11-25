import pandas as pd
import os
from data_access.order_repository import *

def get_chassis_matrix():
    order_connector = OrderRepository()
    columns_data = [
        'OrderId', 'ChassisNumber', 'Parts', 'DATs', 'STDs', 'Straights',
        'TextAmounts'
    ]
    print("Loading data from Order database...")
    data = order_connector.GetOrderChassisMapping()
    print("%.2f lines are loaded." % len(data))
    df_data = pd.DataFrame.from_records(data, columns=columns_data)
    print("Writing data to chassis_matrix.xlsx...")
    dirname = os.path.dirname(os.path.realpath(__file__))
    df_data.to_excel(os.path.join(dirname, "chassis_matrix.xlsx"))
    print("Done.")

if __name__ == "__main__":
    get_chassis_matrix()