'''
import board
import busio
import sdcardio
import os
import storage
#import adafruit_sdcard
import digitalio

class Log:

    def __init__(self):
        # self.sdcard = None
        self.SD_CS = board.D10
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        #self.sd = sdcardio.SDCard(board.SPI(), self.SD_CS)
        self.vfs = storage.VfsFat(self.sd)
        #self.spi = busio.SPI(board.D25, board.D24, board.D23)
        #self.cs = digitalio.DigitalInOut(self.SD_CS)
        #self.logfile = None
        try:
            #self.sdcard = adafruit_sdcard.SDCard(self.spi, self.cs)
            #self.vfs = storage.VfsFat(self.sdcard)
            #storage.mount(vfs, "/sd")
            # self.vfs = storage.VfsFat(self.sdcard)
            storage.mount(self.vfs, "/sd")
            # self.logfile = open("/sd/log.txt", "a")
            os.listdir('/sd')
        except Exception as e:
            print("Failed to initialize SD card: ", e)

    def write(self, msg):
        try:
            with open("/sd/test.txt", "a") as f:
                f.write(msg)
                #self.logfile.write(msg)
        except Exception as e:
            print("Log: ", e)

    def close(self):
        try:
            self.logfile.close()
        except Exception as e:
            print("Log: ", e)

    '''
'''
    # This helper function will print the contents of the SD
    def print_directory(self, path, tabs=0):
        for file in os.listdir(path):
            stats = os.stat(path + "/" + file)
            filesize = stats[6]
            isdir = stats[0] & 0x4000

            if filesize < 1000:
                sizestr = str(filesize) + " bytes"
            elif filesize < 1000000:
                sizestr = "%0.1f KB" % (filesize / 1000)
            else:
                sizestr = "%0.1f MB" % (filesize / 1000000)

            prettyprintname = ""
            for _ in range(tabs):
                prettyprintname += "   "
            prettyprintname += file
            if isdir:
                prettyprintname += "/"
            print("{0:<40} Size: {1:>10}".format(prettyprintname, sizestr))

            # recursively print directory contents
            if isdir:
                print_directory(path + "/" + file, tabs + 1)
log = Log()
'''
