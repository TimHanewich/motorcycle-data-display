import machine
import pico_i2c_lcd
import time

# Get LCD's I2C address
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17)) # change the numbers here to your I2C interface!
print("I2C Scan: " + str(i2c.scan()))
addr = i2c.scan()[0]
print("I will assume this is the I2C address of your LCD: " + str(addr) + " (" + str(hex(addr)) + ")")

# set up LCD interface
lcd = pico_i2c_lcd.I2cLcd(i2c, addr, 2, 16) # 2 is the height, 16 is the width (in # of characters)

# set up adc to read voltage of battery (input)
adc = machine.ADC(26)
carry:int = adc.read_u16()
alpha:float = 0.96

def adc_to_supply_volts(adc_val:int) -> float:
    """Converts the read ADC voltage to the supply voltage, based on this unique system, its current consumption, and test results gathered."""
    m:float = 0.00025018479005
    b:float = -0.04562527564001
    return (m * adc_val) + b      # y = mx + b

while True:
    
    val = adc.read_u16()
    carry = int((carry * alpha) + (val * (1 - alpha)))
    volts:float = adc_to_supply_volts(carry)

    # prepare line 1 (16 chars)
    line1:str = str(val) + ", " + str(carry)
    while len(line1) < 16:
        line1 = line1 + " "

    # prepare line 2 (16 chars)
    line2:str = str(round(volts, 2)) + " volts"
    while len(line2) < 16:
        line2 = line2 + " "
    
    # show and wait
    lcd.putstr(line1 + line2)
    time.sleep(0.25)
    