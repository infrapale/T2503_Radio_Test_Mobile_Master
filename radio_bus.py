# Radio Bus Functions
import time
import board
import busio
import asyncio


class radio_bus:
    def __init__(self, _uart ):    
        # Create a GPS module instance.
        self.uart = _uart
        
    def task(self):
