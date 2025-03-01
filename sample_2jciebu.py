import serial
import time
from datetime import datetime
import sys
import os
import csv
import logging

# Configure the logger
logging.basicConfig(filename='omron.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# LED display rule. Normal On.
DISPLAY_RULE_NORMALLY_ON = 1

# LED display rule. Normal Off.
DISPLAY_RULE_NORMALLY_OFF = 0


def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def calc_crc(buf, length):
    """
    CRC-16 calculation.

    """
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1):
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return (bytearray([crcL, crcH]))


def print_latest_data(data):
    # logging.info('def print_latest_data(data) called.')
    time_measured = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    temperature = relative_humidity = ambient_light = sound_noise = discomfort_index = heat_stroke = vibration_information = 'N/A'
    # print measured latest value.
    try: 
        
        temperature = str( s16(int(hex(data[9]) + '{:02x}'.format(data[8], 'x'), 16)) / 100)
        relative_humidity = str(int(hex(data[11]) + '{:02x}'.format(data[10], 'x'), 16) / 100)
        ambient_light = str(int(hex(data[13]) + '{:02x}'.format(data[12], 'x'), 16))
        sound_noise = str(int(hex(data[19]) + '{:02x}'.format(data[18], 'x'), 16) / 100)
        discomfort_index = str(int(hex(data[25]) + '{:02x}'.format(data[24], 'x'), 16) / 100)
        heat_stroke = str(s16(int(hex(data[27]) + '{:02x}'.format(data[26], 'x'), 16)) / 100)
        vibration_information = str(int(hex(data[28]), 16))
    except IndexError as e: 
        logging.warning('caught byte error: %s', e)

    logging.info('calc of bytes to set data.')

    with open(file_today, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time_measured, temperature, relative_humidity, ambient_light, sound_noise, discomfort_index, heat_stroke, vibration_information])
        
        logging.info('csv file opened to append data')

    # prints to terminal 
    print("")
    print("Time measured:" + time_measured)
    print("Temperature:" + temperature)
    print("Relative humidity:" + relative_humidity)
    print("Ambient light:" + ambient_light)
    print("Sound noise:" + sound_noise)
    print("Discomfort index:" + discomfort_index)
    print("Heat stroke:" + heat_stroke)
    print("Vibration information:" + vibration_information)

def restart_program_file(base_name): # if program restarts , to add counter to same day file 
    logging.info('Checking for existing CSV files to prevent overwriting.')
    counter = 1
    file_name = f"{base_name}.csv"
    
    while os.path.isfile(file_name):
        file_name = f"{base_name}-{counter}.csv"
        counter +=1
        logging.warning(f'File exists. Creating a new file with counter: {file_name}')
    
    return file_name

def now_utc_str():
    """
    Get now utc.
    """
    return datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")


if __name__ == '__main__':

    # Serial communication setup
    max_retries = 10
    retries = 0
    ser = None  # Initialize serial object as None

    # Attempt to establish serial communication
    while retries < max_retries: 
        try:
            ser = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE)
            logging.info('Serial communication established successfully.')
            ser.reset_input_buffer # resets input after establishing successfully 
            
            break  # Exit loop if successful
        except Exception as e:
            logging.warning(f'Attempt {retries + 1} to establish serial communication failed: {e}')
            time.sleep(1)
            retries += 1
            
    # Exit program if serial communication fails
    if ser is None or retries >= max_retries:  
        logging.error('Failed to establish serial communication after maximum retries. Exiting program.')
        sys.exit()

    # File initialization after successful serial communication 
    # time.sleep(5)
    date_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_today = restart_program_file(date_str)
    logging.info(f'File created for data logging: {file_today}')

    # Write header if it's a new file
    if not os.path.isfile(file_today):  
        with open(file_today, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time measured', 'Temperature', 'Relative humidity', 'Ambient light', 'Sound noise', 'Discomfort index', 'Heat stroke', 'Vibration'])
            logging.info(f'Header written to CSV file: {file_today}')

    # Begin data acquisition
    start_time = time.time()
    led_on = True
    try:
        logging.info('Turning on LED (green).')
        command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_ON, 0x00, 0, 255, 0])
        command = command + calc_crc(command, len(command))
        ser.write(command)
        time.sleep(0.1)
        ret = ser.read(ser.inWaiting())

        while ser.isOpen():
            # logging.info('Sending command to acquire sensor data.')
            command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
            command = command + calc_crc(command, len(command))
            ser.reset_input_buffer() # empties incoming buffer of serial port 
            ser.write(command)
            time.sleep(0.1)
            data = ser.read(ser.inWaiting())
            print_latest_data(data)

            if led_on and time.time() - start_time >= 8:
                logging.info('Turning off LED after timeout.')
                command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_OFF, 0x00, 0, 0, 0])
                command = command + calc_crc(command, len(command))
                ser.write(command)
                time.sleep(0.1)
                led_on = False

            time.sleep(10)  # Read every 10 seconds, pauses the program

    except KeyboardInterrupt:
        logging.info('Exiting program due to KeyboardInterrupt.')
        sys.exit()

    logging.info('Program finished.')
