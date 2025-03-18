
class BusMaster:
    def __init__(self,uart_radio):
        self.uart_radio = uart_radio
        print("Initializing bus master...")


    def send(self, msg):
        print("BusMaster sending message:") 
        print(msg['radio'], msg['pwr'])
        bus_msg = "<,R,{},P,{},#,{},>\n".format(msg['radio'], msg['pwr'], msg['nbr'])
        print(bus_msg)
        self.uart_radio.write(bus_msg.encode())

    def receive(self):
        print("BusMaster receiving message...")
        return "BusMaster message received"
    
# bus_master = BusMaster()

