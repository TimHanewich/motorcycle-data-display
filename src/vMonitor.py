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

while True:
    
    val = adc.read_u16()
    carry = int((carry * alpha) + (val * (1 - alpha)))
    
    # show and wait
    lcd.clear()
    lcd.putstr(str(val) + ", " + str(carry))
    time.sleep(0.25)
    