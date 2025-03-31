
import data

class BusMaster:
    def __init__(self,uart_radio):
        self.uart_radio = uart_radio
        self.remote_rssi = 0
        print("Initializing bus master...")


    def set_node_type_remote(self, msg):
        print("BusMaster set node type Remote:") 
        bus_msg = "<,A,R,{},P,{},N,{},S,0,T,0,>\n".format(msg['radio'], msg['pwr'], msg['nbr'])
        print(bus_msg)
        self.uart_radio.write(bus_msg.encode())

    def send(self, msg):
        print("BusMaster sending message:") 
        print(msg['radio'], msg['pwr'])
        bus_msg = "<,B,R,{},P,{},N,{},S,0,T,{},>\n".format(msg['radio'], msg['pwr'], msg['nbr'],data.last_rssi)
        print(bus_msg)
        self.uart_radio.write(bus_msg.encode())

    def receive(self):
        # print("BusMaster receiving message...")
        in_msg = None
        if self.uart_radio.in_waiting > 0:
            in_msg = self.uart_radio.readline()
            # print("BusMaster received message: ",in_msg)
        return in_msg
    
# bus_master = BusMaster()

