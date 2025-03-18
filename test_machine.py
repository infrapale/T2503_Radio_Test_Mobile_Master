import data

class TestMachine:
    def __init__(self, bus_master):
        self.bus_master = bus_master    
        self.running = False
        self.state = 0
        self.msg_nbr = 0
        self.cmd_array = [
            {'radio': data.LORA_433, 'pwr': 5},
            {'radio': data.LORA_433, 'pwr': 10},
            {'radio': data.LORA_433, 'pwr': 14},
            {'radio': data.LORA_433, 'pwr': 20},
            {'radio': data.LORA_868, 'pwr': 5},
            {'radio': data.LORA_868, 'pwr': 10},
            {'radio': data.LORA_868, 'pwr': 14},
            {'radio': data.LORA_868, 'pwr': 20},
            {'radio': data.RFM_433, 'pwr': 5},
            {'radio': data.RFM_433, 'pwr': 10},
            {'radio': data.RFM_433, 'pwr': 14},
            {'radio': data.RFM_433, 'pwr': 20}
        ]
        self.array_indx = 0

    def state_machine(self):
        wait_sec = 1
        if not self.running:
            print("Starting state machine...")
            self.running = True
        else:
            print("test_machine state: ", self.state)
            if self.state == 0:
                print("State 0")
                self.state = 10
            elif self.state == 10:
                print("State 10")
                self.state = 20
            elif self.state == 20:
                print("State 20")
                cmd = {'radio': self.cmd_array[self.array_indx]['radio'], 
                    'pwr': self.cmd_array[self.array_indx]['pwr'], 'nbr': self.msg_nbr}
                self.bus_master.send(cmd)
                self.msg_nbr += 1
                self.array_indx += 1
                if self.array_indx >= len(self.cmd_array):
                    self.array_indx = 0
                wait_sec =5.0
            elif self.state == 30:
                print("State 30")
                for cmd in cmd_array:
                    bus_master.send(cmd)
                self.state = 0

        return wait_sec

    def stop(self):
        if self.running:
            print("Stopping state machine...")
            self.running = False
        else:
            print("State machine is not running.")


