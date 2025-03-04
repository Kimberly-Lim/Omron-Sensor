# Omron-Sensor
Program for evaluating Omron's sensor 2JCIE-BU with Raspberry Pi Zero. 

2JCIE_BU is a multifunction sensor module that can be used for sensing various environmental information such as tempertaure, light, and sound. This program allows the user to plug in the USB to the Raspberry Pi to direct power and automatically collect and store data. 

## Description
* sample_2jciebu.py is a program that can acquire sensing data with the USB serial interface and stores the data into dated .csv files. On initial bootup the LED will light up then turn off to indicate a power source has been connected. The LED then will initally light up green for 8 seconds then turn off when data is being read and processed.
* Temp_Characterization_omron.m is a MATLAB script to visualize data from the omron sensor. It takes the .csv file name and outputs three graphs of temperature, sound, and light. 

## Dependencies
* [Python3](https://www.python.org/)
* [pyserial](https://pythonhosted.org/pyserial/pyserial.html#installation)


## Set Up and Extraction 
* 1. Plug in cable to powerbank to turn on raspberry pi and sensor.
  2. Once sensor lights up different colors and turns off, wait about 1 minute for sensor to turn green for 8 seconds then turn off. Sensor is now reading and collecting data.
  3. To extract data, unplug power cable and plug in microSD card to computer and open software [DiskInternals](https://www.diskinternals.com/linux-reader/). 
     
## License
Copyright (c) OMRON Corporation. All rights reserved.
