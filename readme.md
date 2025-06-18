# Motorcycle Data Display
Displaying battery voltage, ambiet temperature, and ambiet humidity.

Example display:
![example](https://i.imgur.com/XnHHV8R.png)

## Voltage Divider
A voltage divider must be used to drop the battery voltage (around 12v) to a range in which the Raspberry Pi Pico can safely read, between 0.0 and 3.3 volts.

I believe the best set up is to have an R1 resistor of **470,000 ohms** and an R2 resistor of **120,000 ohms**. This drops the voltage down to 20.34% of itself.

|Voltage|Divided|
|-|-|
|15|3.051|
|10|2.033|

## Design
"The box" will contain:
- LCD Display
- Raspberry Pi Pico
- LM2596 Voltage Converter
- Voltage divider

Box inputs:
- Battery +
- Battery - 
- DHT22 +
- DHT22 - 
- DHTT data

## Other Resources
- [Excellent 16x2 LCD Dummy on Sketchfab](https://sketchfab.com/3d-models/lcd-2004-16x2-hd44780-dummy-ea053f7f3c7045e4940769e17f48a0d0)
    - I uploaded it to Thingiverse [here](https://www.thingiverse.com/thing:7069861)
    - I backed it up on GitHub [here](https://github.com/TimHanewich/motorcycle-data-display/releases/download/2/LCD.stl)