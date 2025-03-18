import board
import busio as io
import adafruit_ht16k33.segments
import adafruit_bme680

import neopixel

i2c = io.I2C(board.SCL, board.SDA)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c,0x76)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

# display = adafruit_ht16k33.segments.Seg14x4(i2c)
display = adafruit_ht16k33.segments.Seg14x4(i2c, address=0x70)
display.fill(0)
display.show()
# display[0] = 'M'
display.show() 
# display.print('-21.2')
display.print('MIFA')
display.show()
display.brightness = 0
led[0] = (255, 0, 0)
print('Temperature: {:.1f} degrees C'.format(sensor.temperature))
print('Gas: {} ohms'.format(sensor.gas))
print('Humidity: {}%'.format(sensor.humidity))
print('Pressure: {}hPa'.format(sensor.pressure))
display.fill(0)
display.print('{:.1f}'.format(sensor.temperature))