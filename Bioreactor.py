class Bioreactor: #container to hold and send values when updated to the MSP board
    def __init__(self):
        self.serial_port = None
        self.speed = 1500
        self.ph = 7
        self.temperature = 32

    def update(self):
        if self.serial_port is not None:
            self.serial_port.send_data('<speed,{}>'.format(self.speed))
            self.serial_port.send_data('<ph,{}>'.format(self.ph))
            self.serial_port.send_data('<temperature,{}>'.format(self.temperature))
            return True
        else: return False
