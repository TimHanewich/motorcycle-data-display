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

## Determining Supply Voltage from the ADC-Read Voltage Divider
A key step in this project is using the read ADC reading to determine the supply voltage (battery voltage). In commit `8ced83096d89e48986466c1a64de321f39fb7256`, I wrote a lightweight script that would simply print the current voltage supply (GP26) reading as well as a moving average to the LCD display. Using this test script, we can observe the ADC reading the Pi is getting at various supply voltages:

|Supply Voltage|Multimeter Voltage Reading|ADC Reading|
|-|-|-|
|15.88 |15.88|63,650|
|15.03|15.04 |60,200|
|14.22|14.23 |57,110|
|13.19|13.21 |53,020|
|12.20|12.20 |48,930|
|11.73|11.75 |47,115|
|11.09|11.11 |44,500|
|10.43|10.45 |41,835|
|9.80|9.82|39,445|
|8.93|8.96|35,980|
|8.07|8.10|32,475|

The table above includes the test results from this experiment. The "Supply Voltage" column contains the voltage my DC power supply claimed it was supplying, the "Multimeter Voltage Reading" column contains the voltage my multimeter was reading, touching the alligator clips, and the "ADC Reading" is the Pi Pico's average reading at that voltage level.

We an see that the relationship between supply voltage is linear. In Excel, we can treat these as a series of X,Y pairs and pass them into the `=LINEST()` function to determine `m` and `b` in the equation `y = mx + b` (estimate the y-intercept and slope). In our experiment, we set a voltage and determined the ADC reading which indeed means the voltage is the independent variable (X) with the reading being the dependent variable (Y). However, for the sake of our project, we want to do the opposite - infer supply voltage *from the ADC reading*. So, when I use Excel's `=LINEST()` function, I am treating the ADC reading as X value and Volts as the Y value.

![linest](https://i.imgur.com/UGsR6Ec.png)

*In the above image, please note the `=LINEST()` function expects y-values FIRST and x-values SECOND*

Result:
- y = 0.00025018479005
- b = -0.04562527564001

So, to infer the supply voltage from the ADC reading, simply multiply the ADC reading by the `y` value above and then add `b`!

## Other Resources
- [Excellent 16x2 LCD Dummy on Sketchfab](https://sketchfab.com/3d-models/lcd-2004-16x2-hd44780-dummy-ea053f7f3c7045e4940769e17f48a0d0)
    - I uploaded it to Thingiverse [here](https://www.thingiverse.com/thing:7069861)
    - I backed it up on GitHub [here](https://github.com/TimHanewich/motorcycle-data-display/releases/download/2/LCD.stl)