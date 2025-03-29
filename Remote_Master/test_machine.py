import data
import time

last_ack = {'radio': 0, 'pwr': 5, 'nbr': 0, 'remote_rssi': 0, 'center_rssi': 0}
class TestMachine:
    def __init__(self, bus_master):
        self.bus_master = bus_master    
        self.running = False
        self.state = 0
        self.msg_nbr = 0
        self.timeout_at = 0
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
    def parse_ack_0(self, in_msg):
        global last_ack
        # b'[,R,2,P,10,#,329,SR,-87,SC,-85,]'
        if in_msg[1] == ord('R'):
            if in_msg[3] == ord('P'):
                last_ack['radio'] = in_msg[5] - ord('0')
                last_ack['pwr'] = in_msg[7] - ord('0')
                last_ack['nbr'] = in_msg[9] - ord('0')
                last_ack['remote_rssi'] = in_msg[11] - ord('0')
                last_ack['center_rssi'] = in_msg[15] - ord('0')
                print("Last Ack: ", last_ack)
            else:
                print("Invalid Ack: ", in_msg)
        else:
            print("Invalid Ack: ", in_msg)

    def parse_ack(self, in_msg):
        global last_ack
        # b'[,R,2,P,10,#,329,S,-87,]
        is_valid = False
        print("parse_ack: ", in_msg)





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
                wait_sec =5.0
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
                self.timeout_at = time.monotonic() + 5    
                self.state = 25
            elif self.state == 25:  
                # empty sent message from buffer
                in_msg = self.bus_master.receive()   
                if in_msg is not None:
                    self.timeout_at = time.monotonic() + 5
                    self.state = 30
                    print(in_msg)
                    self.timeout_at = time.monotonic() + 5
                    # b'[,R,2,P,10,#,329,SR,-87,SC,-85,]
                elif time.monotonic() > self.timeout_at:
                    print("Ack Timeout")
                    self.state = 10
                
            elif self.state == 30:
                print("State 30")
                in_msg = self.bus_master.receive()
                if in_msg is not None:
                    self.state = 10
                    print(in_msg)
                    self.parse_ack(in_msg)
                    # b'[,R,2,P,10,#,329,S,-87,]
                elif time.monotonic() > self.timeout_at:
                    print("Ack Timeout")
                    self.state = 10
        return wait_sec

    def stop(self):
        if self.running:
            print("Stopping state machine...")
            self.running = False
        else:
            print("State machine is not running.")


