import time
import board
import busio
import asyncio
import adafruit_gps

gps_data = {'satellites':0}


class gps_x:
    def __init__(self, _uart ):    
        # Create a GPS module instance.
        self.uart = _uart
        self.gps = adafruit_gps.GPS(self.uart, debug=False)  # Use UART/pyserial
        # gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Turn on the basic GGA and RMC info + VTG for speed in km/h
        # gps.send_command(b"PMTK314,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Turn on just minimum info (RMC only, location):
        # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b"PMTK220,1000")
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!
        # gps.send_command(b'PMTK220,2000')
        # You can also speed up the rate, but don't go too fast or else you can lose
        # data during parsing.  This would be twice a second (2hz, 500ms delay):
        # gps.send_command(b'PMTK220,500')

        # Main loop runs forever printing the location, etc. every second.

         
    def read_signal(self):
        # Make sure to call gps.update() every loop iteration and at least twice
        # as fast as data comes from the GPS unit (usually every second).
        # This returns a bool that's true if it parsed new data (you can ignore it
        # though if you don't care and instead look at the has_fix property).
        self.gps.update()
        # Every second print out current location details if there's a fix.
        if not self.gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            gps_data['satellites'] = 0
        else:            # We have a fix! (gps.has_fix is true)
            gps_data['satellites'] = self.gps.satellites

            # Print out details about the fix like location, date, etc.
            print("=" * 40)  # Print a separator line.
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    self.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    self.gps.timestamp_utc.tm_min,  # month!
                    self.gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(self.gps.latitude))
            print("Longitude: {0:.6f} degrees".format(self.gps.longitude))
            print(
                "Precise Latitude: {} degs, {:2.4f} mins".format(
                    self.gps.latitude_degrees, self.gps.latitude_minutes
                )
            )
            print(
                "Precise Longitude: {} degs, {:2.4f} mins".format(
                    self.gps.longitude_degrees, self.gps.longitude_minutes
                )
            )
            print("Fix quality: {}".format(self.gps.fix_quality))
            # Some attributes beyond latitude, longitude and timestamp are optional
            # and might not be present.  Check if they're None before trying to use!
            if self.gps.satellites is not None:
                print("# satellites: {}".format(self.gps.satellites))
            if self.gps.altitude_m is not None:
                print("Altitude: {} meters".format(self.gps.altitude_m))
            if self.gps.speed_knots is not None:
                print("Speed: {} knots".format(self.gps.speed_knots))
            if self.gps.speed_kmh is not None:
                print("Speed: {} km/h".format(self.gps.speed_kmh))
            if self.gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(self.gps.track_angle_deg))
            if self.gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(self.gps.horizontal_dilution))
            if self.gps.height_geoid is not None:
                print("Height geoid: {} meters".format(self.gps.height_geoid))
                
    def get_nbr_satellites(self):
        return
    

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps_x = gps_x(uart)
 

