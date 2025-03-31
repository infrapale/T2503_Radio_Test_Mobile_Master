import data
import time
import board
import neopixel



ORDER = neopixel.RGB  # pixel color channel order
COLOR_RED       = (255, 0, 0)  
COLOR_GREEN     = (0, 255, 0)  
COLOR_BLUE      = (0, 0, 255)  
COLOR_CYAN      = (255, 255, 0)  
COLOR_MAGENTA   = (0, 255, 255)  
COLOR_BLACK     = (0, 0, 0)  


led = neopixel.NeoPixel(board.NEOPIXEL, 1,  pixel_order=ORDER)


last_ack = {'radio': 0, 'pwr': 5, 'nbr': 0, 'remote_rssi': 0, 'center_rssi': 0}
class TestMachine:
    def __init__(self, bus_master):
        self.bus_master = bus_master    
        self.running = False
        self.state = 0
        self.new_state = 0
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
        self.array_indx = 8
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

    def set_radio_color(self, radio):
        if radio == data.LORA_433:
            led[0] = COLOR_RED 
        elif radio == data.LORA_868:
            led[0] = COLOR_GREEN
        elif radio == data.RFM_433:
            led[0] = COLOR_BLUE 



    def state_machine(self):
        wait_sec = 1
        print("Test State: ", self.state)
        if not self.running:
            print("Starting state machine...")
            self.running = True
        else:
            if self.state == 0:
                self.new_state = 5
            elif self.state == 5:
              
                cmd = {'radio': data.RFM_433, 'pwr': 5, 'nbr': 0} 
                self.bus_master.set_node_type_remote(cmd)
                self.new_state = 10
            elif self.state == 10:

                wait_sec =10.0
                self.new_state = 20

            elif self.state == 20:
                self.set_radio_color(self.cmd_array[self.array_indx]['radio'])
                cmd = {'radio': self.cmd_array[self.array_indx]['radio'], 
                    'pwr': self.cmd_array[self.array_indx]['pwr'], 'nbr': self.msg_nbr}
                self.bus_master.send(cmd)
                self.msg_nbr += 1
                self.array_indx += 1
                if self.array_indx >= len(self.cmd_array):
                    self.array_indx = 0
                self.timeout_at = time.monotonic() + 1    
                self.new_state = 25

            elif self.state == 25:  
                # empty own sent message from buffer
                in_msg = self.bus_master.receive()   
                if in_msg is not None:
                    self.new_state = 30
                    print(in_msg)
                    self.timeout_at = time.monotonic() + 5
                    # b'[,R,2,P,10,#,329,SR,-87,SC,-85,]
                elif time.monotonic() > self.timeout_at:
                    print("Own message timeout")
                    self.new_state = 10
                
            elif self.state == 30:
                in_msg = self.bus_master.receive()
                if in_msg is not None:
                    self.new_state = 10
                    print(in_msg)
                    self.parse_ack(in_msg)
                    # b'[,R,2,P,10,#,329,S,-87,]
                elif time.monotonic() > self.timeout_at:
                    print("Ack Timeout")
                    self.new_state = 10

        self.state = self.new_state 
        return wait_sec

    def stop(self):
        if self.running:
            print("Stopping state machine...")
            self.running = False
        else:
            print("State machine is not running.")


