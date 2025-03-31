# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import time
import board
import busio
import asyncio
# import adafruit_gps
from adafruit_ht16k33 import segments


from gps_x import gps_x
from gps_x import gps_data
from test_machine import TestMachine   
from bus_master import BusMaster
import data

uart_radio = busio.UART(board.D5, board.D6, baudrate=9600)
uart_bt = busio.UART(board.D12, board.D11, baudrate=9600)


display = segments.Seg14x4(board.I2C())  # uses board.SCL and board.SDA
# i2c = board.I2C()  # uses board.SCL and board.SDA
# Create a second UART on alternate pins (example: GPIO 5 and 6)

bus_master = BusMaster(uart_radio)
tm = TestMachine(bus_master)

display.marquee("T2503 LoRa Test Mobile Master", loop=False)

async def gps_read():
    # uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
    # gps_x = gps_x(uart)
    while True:
        gps_x.read_signal()
        str14 = "SA{}".format(gps_data['satellites'])
        print(str14)
        await asyncio.sleep(10.0)

async def bus_cmd():
    while True:
        #uart_radio.write(b"Hello from radio UART!")
        #uart_bt.write(b"Hello from bluetooth UART!")       
        await asyncio.sleep(1.0)

async def test_machine():
    while True:
        #uart_radio.write(b"Hello from radio UART!")
        #uart_bt.write(b"Hello from bluetooth UART!")
        sleep_sec = tm.state_machine() 
        await asyncio.sleep(sleep_sec)

async def main():
    gps_task = asyncio.create_task(gps_read())
    bus_cmd_task = asyncio.create_task(bus_cmd())
    test_task = asyncio.create_task(test_machine())

    await asyncio.gather(gps_task,bus_cmd_task,test_task)  
    print("done")

asyncio.run(main())

        