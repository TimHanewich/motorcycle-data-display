import machine
import time
import pico_i2c_lcd
import dht
import math

# set up PI LED
led = machine.Pin(25, machine.Pin.OUT)
led.on() # turn on during short boot sequence to confirm it is on

# create problem sequence, an infinite loop of flashes
def PROBLEM() -> None:
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

# method for converting ADC reading into inferred voltage
# this is VERY SPECIFIC to this project. These vals were precisely determined through tests. See readme for more info.
def adc_to_supply_volts(adc_val:int) -> float:
    """Converts the read ADC voltage to the supply voltage, based on this unique system, its current consumption, and test results gathered."""
    m:float = 0.00025018479005
    b:float = -0.04562527564001
    return (m * adc_val) + b      # y = mx + b

# place the whole thing in a massive Try bracket to handle errors
try:


    # Set up LCD
    i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
    i2c_scan:list[int] = i2c.scan()
    if 39 not in i2c_scan: # if the 16x2 LCD display is not found on the i2c bus, there is a wiring issue
        PROBLEM() # infinite problem display
    lcd = pico_i2c_lcd.I2cLcd(i2c, 39, 2, 16) # height of 2 lines, width of 16 characters)
    lcd.backlight_on()
    lcd.putstr("Loading...")

    # store degree symbol as a custom character (it doesn't work as is)
    degree:bytes = bytes([0b00110, 0b01001, 0b01001, 0b00110, 0b00000, 0b00000, 0b00000, 0b00000])
    lcd.custom_char(0, degree) # store the degre symbol as custom char #0

    # create function for displaying data
    def display_data(temp:float, humidity:float, voltage:float) -> None:
        """Provide temperature as the temp in fahrenheight (i.e. 98.7), provide humidity as a relative humidity percentage (i.e. 0.65 for 65% RH), and voltage as a voltage (i.e. 12.2)"""
        
        # there is no need to clear the LCD because every character that is NOT used will be written over with an empty space
        
        # assemble line 1 (voltage)
        vDisplay:str = str(round(voltage, 1)) + " v"
        vSpacesBefore:int = math.floor((16 - len(vDisplay)) / 2)
        vSpacesAfter:int = 16 - vSpacesBefore - len(vDisplay)
        line1:str = (' ' * vSpacesBefore) + vDisplay + (' ' * vSpacesAfter)
        lcd.putstr(line1)
        
        # assemble line 2 (temp + humidity)
        tValDisplay:str = "?" # default to "?" in case there is an issue (i.e. it was supplied as null)
        if temp != None:
            tValDisplay = str(round(temp, 1))
        hValDisplay:str = "?" # default to "?" in case there is an issue (i.e. it was supplied as null)
        if humidity != None:
            hValDisplay = str(round(humidity * 100, 1))
        tDisplay:str = tValDisplay + " " + chr(0) + "F"
        hDisplay:str = hValDisplay + " %H"
        SpacesBetween = 16 - len(tDisplay) - len(hDisplay) # how many spaces to put in between
        line2:str = tDisplay + (' ' * SpacesBetween) + hDisplay
        
        # print both lines! (both should be 16 characters wide)
        lcd.move_to(0, 0)
        lcd.putstr(line1 + line2)

    # Set up DHT22
    sensor = dht.DHT22(machine.Pin(2))

    # Set up ADC for reading the battery supply voltage (hooked up via voltage divider)
    batADC = machine.ADC(26)
    batADC_RA:int = None # the variable that will be used to contain the rolling avg
    alpha:float = 0.96 # will be used for "smoothing out" (rolling average) the incoming ADC reading... the higher this value is, the smoother it is

    # go into infinite loop display
    while True:

        # read the battery voltage
        batADC_val:int = batADC.read_u16()
        if batADC_RA == None:
            batADC_RA = batADC_val
        else:
            batADC_RA = int((batADC_RA * alpha) + (batADC_val * (1 - alpha)))
        supply_voltage:float = adc_to_supply_volts(batADC_RA) # convert the moving avg. ADC reading into the supply voltage
        print("Supply voltage: " + str(supply_voltage))
        
        # read the DHT22 values (or at least try to)
        TimesTried:int = 0
        tempF:float = None # temperature, in celsius
        humidity:float = None # relative humidity
        while tempF == None and humidity == None and TimesTried < 5: # limit the number of times tried - you can change it here
            try:
                sensor.measure()
                tempC = sensor.temperature()
                tempF = (tempC * (9/5)) + 32 # convert Celcius (what the DHT22 provides) into Fahrenheit
                humidity = sensor.humidity() / 100 # relative humidity, but divide by 100 because the DHT22 sensor class provides it like "56.7", but I prefer to handle it as a value between 0.0 and 1.0
                print("TempF: " + str(tempF))
                print("Humidity: " + str(humidity))
            except:
                print("Failed to read from DHT22 on attempt # " + str(TimesTried))
                TimesTried = TimesTried + 1
                time.sleep(0.1)

        # display!
        display_data(tempF, humidity, supply_voltage)

        # wait
        time.sleep(1.0)
    

except: # if there is an unhandled problem...
    PROBLEM() # ... just show the problem sequence on the Pi's LED