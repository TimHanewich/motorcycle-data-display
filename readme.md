# Motorcycle Data Display
This project features a 3D printed dashboard-like system mounted on a motorcycle, using a Raspberry Pi Pico to monitor and display real-time motorcycle battery voltage, ambient temperature, and humidity. It uses a 16x2 LCD and is powered directly by the motorcycle's battery.

![example](https://i.imgur.com/Inj0Ljx.jpeg)

## Required Hardware
- 🖨️ Custom 3D printed enclosure (.STL files included below)
- 🔌[Toggle Power Switch](https://a.co/d/0Lbv3p1)
- 📟 [16x2 LCD Display](https://a.co/d/b4bnMaQ)
- 🔌 Voltage Divider circuit to measure battery voltage (*read more below*)
- 🌡️ [DHT22 sensor](https://a.co/d/ewYQhxm) for ambient temperature and humidity
- 🧠 [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) for control logic
- ⚡ [LM2596 buck converter](https://a.co/d/bLv2FjF)
- 🔋 Powered by the motorcycle's 12V battery
    - You can directly wire it to your battery terminals or use [an SAE connector](https://a.co/d/0mAilbJ) connected to your battery's tender if it has one, like I did.

## Wiring Diagram
I provide the full wiring diagram as [wiring.drawio](./wiring.drawio) in this repository. Visit [draw.io](https://draw.io) to open this file.

![wiring](https://i.imgur.com/RtzVz5e.png)

## Source Code
Once you get your hardware wired up according to the diagram above, you can load [the code](./src/) directly onto the Raspberry Pi Pico.

All three files are required to be placed directly in the root directory.

## 3D Printed Enclosure
I designed and 3D-printed the enclosure for this project. You can find the STL files available for download for free on Thingiverse [here](https://www.thingiverse.com/thing:7082009).

This enclosure will contain all hardware:
- 16x2 LCD Display
- Power Switch
- Raspberry Pi Pico
- Voltage divider
- LM2596 Voltage Converter (drops battery's voltage down to a stable 5v supply for Raspberry Pi, display, and sensors)

The enclosure will have **five** wires running in/out of it (a hole in the enclosure accomodates this):
- Motorcycle Battery +
- Motorcycle Battery - 
- DHT22 Power Supply +
- DHT22 Power Supply - 
- DHT22 data line

## Voltage Divider
A voltage divider must be used to drop the battery voltage (around 12v for a standard motorcycle battery) to a range in which the Raspberry Pi Pico can safely read, between 0.0 and 3.3 volts. You can read more about voltage dividers [here](https://learn.sparkfun.com/tutorials/voltage-dividers/all).

I purchased [this package of resistors](https://a.co/d/0yozjyX) and made a voltage divider using a **22,000 ohm** R1 resistor and a **5,600 ohm** R2 resistor. This drops the voltage down to 20.29% of itself.

|Voltage|Divided|
|-|-|
|15|3.04|
|10|2.029|

As seen above, the effects of this voltage divider effectively drop the input voltage down to something that is safe to provide to the Pi.

**IMPORTANT: With this voltage divider configuration, the absolute MAXIMUM supply voltage is approximately 16 volts. Beyond this, the divided voltage will exceed 3.3 volts, the maximum the Raspberry Pi can handle on the ADC pins. Exceeding this value may cause damage to the Pi!**

## Notable Commits
|Commit|Note|
|-|-|
|`8ced83096d89e48986466c1a64de321f39fb7256`|Basic code for displaying voltage supply ADC reading to display|
|`061c1e2b2cda765a97523a54c5203dea3d97f5c9`|Basic code for displaying voltage supply ADC reading to display, but with the voltage being calculated and display as well|

## Other Resources
- I modeled my 16x2 LCD enclosure around [this excellent dummy model](https://www.thingiverse.com/thing:3505029)
    - I originally designed it around this [16x2 LCD Dummy from Sketchfab](https://sketchfab.com/3d-models/lcd-2004-16x2-hd44780-dummy-ea053f7f3c7045e4940769e17f48a0d0) (backed up [here](https://github.com/TimHanewich/motorcycle-data-display/releases/download/2/LCD.stl))but realized that this one is not correct, it's dimensions are off! Do NOT use this one!
- Link to this repository, shortened with bit.ly: [bit.ly/3SXN4vF](bit.ly/3SXN4vF)