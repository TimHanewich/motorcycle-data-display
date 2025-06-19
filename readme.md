# Motorcycle Data Display
Displaying battery voltage, ambiet temperature, and ambiet humidity.

Example display:
![example](https://i.imgur.com/XnHHV8R.png)

## Voltage Divider
A voltage divider must be used to drop the battery voltage (around 12v) to a range in which the Raspberry Pi Pico can safely read, between 0.0 and 3.3 volts.

I believe the best set up is to have an R1 resistor of **22,000 ohms** and an R2 resistor of **5,600 ohms**. This drops the voltage down to 20.29% of itself.

|Voltage|Divided|
|-|-|
|15|3.04|
|10|2.029|

## Design
"The box" will contain:
- LCD Display
- Raspberry Pi Pico
- LM2596 Voltage Converter
- Voltage divider
- Power Switch

Box inputs:
- Battery +
- Battery - 
- DHT22 +
- DHT22 - 
- DHTT data

## Power Consumption
In the event this system was independently left *on* and was continuously drawing current from the motorcycle, for how long can it run before it begins to pose a risk to the ability of the battery to start the motorcycle (not deplete the battery too much)?

Let's look at a "worst case scenario"...

This system's power consumption estimate:
|Component|Current Consumption, mA|
|-|-|
|RPi Pico|40|
|LCD|25|
|DHT22|3|

For the components used in this system, that is a total of **68 mA**, or **0.068 A** of current. At a nominal 5 volts, that is **0.34 watts**.

However, this system will be powered by a 12v battery, so an LM2596 converter will be used to *lower* the 12v supply voltage to the 5v that is safely needed. That LM2596 does not have perfect efficiency, so we must account for that in our calculation. So, I'm adding an additional 33% of power consumption on top of that previous 0.34 watt figure, arriving at **0.452 watts**. That is very conservative (I doubt it will actually be 33% inefficient).

[The motorcycle battery I have](https://a.co/d/evGOHXQ) is 12v, 8Ah, for a total stored energy of 96 watt hours. When fully charged, the voltage is 12.8v - 13.0v. When fully deplted, the voltage is roughly 11.8v - 11.9v. At 12.4v (70-75% charge), many batteries can start to struggle with cold engine starts, so that is the bar we do **not** want to drop below.

So, this system can safely draw power from the battery down to 75% of the battery's capacity. In my case with my battery, 25% of the power it holds would be 2 Ah (25% of 8 Ah), or 24 watt hours (2 Ah x 12v) of power.

With **24 watt hours** to safely consume without posing risk and a parasitic power draw of **0.452 watts**, that leaves us with **~53 hours** that this system can be left on, drawing power from the battery, without posing a risk to depleting the battery to a level in which it cannot cold start the engine. 

Again, this is a very conservative, worst-case scenario calculation! In reality, the current consumption of this system will be less than we budgeted for, the efficiency of the LM2596 will be greater than we planned for, and we can reliably use more power reserves of the battery without introducing risk of it not starting... but better to be on the safe side!

## Other Resources
- [Excellent 16x2 LCD Dummy on Sketchfab](https://sketchfab.com/3d-models/lcd-2004-16x2-hd44780-dummy-ea053f7f3c7045e4940769e17f48a0d0)
    - I uploaded it to Thingiverse [here](https://www.thingiverse.com/thing:7069861)
    - I backed it up on GitHub [here](https://github.com/TimHanewich/motorcycle-data-display/releases/download/2/LCD.stl)