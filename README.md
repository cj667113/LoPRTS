# LoPRTS V1.3 [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=TZJP4R4BUD6JA&currency_code=USD&source=url)

Low Power Remote Temperature Sensor
![LoPRT Board](https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/LoPRTS_board_1.png?raw=true)

This project was designed with the ESP32-WROOM module with Micropython. Essentially, this project allows for Low Powered Remote Temperature Sensor to be used in conjection with PRTG. By installing an HTTP Push Device in PRTG, you will be allowed to point and push data to the sensor. This will allow us to put the ESP32 into deep sleep to conserve battery power, and allow the device to wake up and report a messurement without worrying about IP addressing and reduce the amount of time the ESP32 has to stay awake.

Included in this project is the custom PCB boards I designed, temperature.py which is the code used to report the measurements, and the STL files for the case.

# LoPRTS V1.3-Current Changes
<b>Hardware:</b>
1. None

<b>Software:</b>
1. MQTT subversion. Included Simple Github OTA Updater (https://github.com/cj667113/simple_github_ota_updater) that will monitor the repository and install new software after each hard-reset.

# Micropython
http://micropython.org/download

I am using micropython version esp32-20190619-v1.11-49-g34c04d231.bin.

I used Esptools.py to connect to the board to erase the board and flash the firmware to it. Hold Key 2 down while pressing Key 1 to enter download mode.

I used Ampy to put the temperature.py code as boot.py on the board. After flashing the board, press Key 1 to reset the board, before uploading with Ampy.

# Wake-up Control Pin
I included P2 as a Touch Pin to force wake the micropython controller. In the designs of my case I used a small piece of copper plate that I had left over from raspberry pi heat sinks to fit the case. Similiar to the link below:

(https://www.amazon.com/Lanpu-Raspberry-Heatsink-Aluminum-cooling/dp/B079K43ZTZ/ref=sr_1_6?crid=2UJHM4N1H8GJ3&keywords=raspberry+pi+heatsink&qid=1551036431&s=gateway&sprefix=raspberry+pi+hea%2Caps%2C152&sr=8-6)

# Power On/Off & Deepsleep
Note that the LoPRTS system works as soon as you attach a power supply, there is no off function, rather there is only deepsleep. That means there has to be reliable WiFi connection or else the system will just search for a WiFi point. I notice that this might be an issue so I am going to update the code to go to deepsleep after I have time. 

# Battery Life
For the PBC board, you can use a linear voltage regulator with the trade off of effeciency to the batteries. I ran the boards on 4-D batteries in parallel and in series to get a battery of 26,000 mah at 3V. I concluded that if the ESP32 took 4 seconds to get through the code and report the data and then we placed the board in deep sleep for 15 minutes then:

250ma (peak current)*(4/(900+4))
<p>250ma*(.004424)=1.106ma
<p>1.106+1 (deep sleep current)=2.106ma
<p>26,000/2.106=12,345 hours
<p>12,345 * 70% (efficency)= 8,642 hours or 360 days on batteries

**Note that Energizer rates their D-Batteries at 20,000mah @ 25ma typical draw, applying this, then the battery life may be even longer than 360 days. **

# MQTT Version

You will need to also upload a setup.txt file to the ESP32. Please look at setup_example.txt for the format. This file should take care of all the information that your unique setup will require.

# PRTG Version

Once you download and setup PRTG, you can install a HTTP Push Data Sensor, so that the ESP32 can send Temperature and Voltage statuses to PRTG. The following is what my graph looks like:

![PRTG_Integration](https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/graph.png?raw=true)

# Fully Assembled
<img src="https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/blue.jpg">
<img src="https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/green.jpg">

![LoPRTS Total](https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/batt.jpg?raw=true)

![LoPRTS_Full](https://github.com/cj667113/LoPRTS/blob/master/LoPRTS_Photos/whole.jpg?raw=true)
