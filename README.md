# Omron-Sensor
Program for evaluating Omron's sensor 2JCIE-BU with Raspberry Pi Zero. 

2JCIE_BU is a multifunction sensor module that can be used for sensing various environmental information such as tempertaure, light, and sound. This program allows the user to plug in the USB to the Raspberry Pi to direct power and automatically collect and store data. 

## Description
* sample_2jciebu.py is a program that can acquire sensing data with the USB serial interface and stores the data into dated .csv files. On initial bootup the LED will light up then turn off to indicate a power source has been connected. The LED then will initally light up green for 8 seconds then turn off when data is being read and processed.
* Temp_Characterization_omron.m is a MATLAB script to visualize data from the omron sensor. It takes the .csv file name and outputs three graphs of temperature, sound, and light. 

## Dependencies
* [Python3]([url](https://www.python.org/))
* [pyserial]([url](https://pythonhosted.org/pyserial/pyserial.html#installation))
## License
Copyright (c) OMRON Corporation. All rights reserved.
