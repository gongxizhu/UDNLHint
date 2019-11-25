class ChassisModel(object):
    def __init__(self, chassis_model):
        self.chassis_model = chassis_model
        self.parts = []
        self.stds = []
        self.dats = []
        self.amount = 0
        self.straight = 0