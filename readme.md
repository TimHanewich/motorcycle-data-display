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