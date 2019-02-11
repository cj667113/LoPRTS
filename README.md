# LoPRTS
Low Power Remote Temperature Sensor

This project was designed with the ESP32-WROOM module with Micropython. Essentially, this project allows for Low Powered Remote Temperature Sensor to be used in conjection with PRTG. By installing an HTTP Push Device in PRTG, you will be allowed to point and push data to the sensor. This will allow us to put the ESP32 into deep sleep to conserve battery power, and allow the device to wake up and report a messurement without worrying about IP addressing and reduce the amount of time the ESP32 has to stay awake.

Included in this project is the custom PCB boards I designed, temperature.py which is the code used to report the measurements, and the STL files for the case.

# Battery Life
For the PBC board, you can use a linear voltage regulator with the trade off of effeciency to the batteries. I ran the boards on 4-D batteries in parallel and in series to get a battery of 26,000 mah at 3V. I concluded that if the ESP32 took 4 seconds to get through the code and report the data and then we placed the board in deep sleep for 15 minutes then:

250ma (peak current)*(4/(900+4))
250ma*(.004424)=1.106ma
1.106+1 (deep sleep current)=2.106ma
26,000/2.106=12,345 hours
12,345 * 70% (efficency)= 8,642 hours or 360 days on batteries

**Note that Energizer rates their D-Batteries at 20,000mah @ 25ma typical draw, applying this, then the battery life may be even longer than 360 days. Also note, that when using LD1117-3.3 TO-220 linear voltage regulator, the component introduces an added 5ma draw.**
