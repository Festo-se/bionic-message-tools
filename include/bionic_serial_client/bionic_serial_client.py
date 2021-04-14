#!/usr/bin/env python3

__author__ = "Marinus Matthias Moerdijk & Timo Schwarzer"
__copyright__ = "Copyright 2020, Festo Coperate Bionic Projects"
__credits__ = ["Timo Schwarzer", "Marinus Matthias Moerdijk"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.6"
__maintainer__ = "Timo Schwarzer"
__email__ = "timo.schwarzer@festo.com"
__status__ = "Experimental"

import serial
import struct

from serial.tools import list_ports
from serial.serialutil import SerialException

import threading
from threading import Lock
import abc
import logging
import time
import platform

from bionic_message_base.bionic_message_base import BionicMessageBase
from bionic_message_tools.bionic_message_tools import BionicMessageHandler

class BionicSerialClient:

    _port = '/dev/ttyUSB0'
    _baud = 2000000
    _send_timeout = 1.0 # Sec
    _shutdown = False
    _max_retries = 5
    
    def __init__(self, message_handler=BionicMessageHandler(),  port='/dev/ttyUSB0', baud=2000000, maxRetries = 5):
        
        # Setup the serial port for different systems
        if platform.system() == "Windows":
            
            # TODO:
            # List COM Ports
            # Select via number one of these
            # Write name into the ftdi description list

            logging.info("Setup COM port for windows")
            #_port = f"USB Serial Port ({port})"             
            self._port = f"({port})"             

        elif platform.system() == "Linux":
            
            logging.info("Setup COM port for linux")
            self._port = port

        self._max_retries = maxRetries
        self._baud = baud
        self.mutex = Lock()
        self.message_handler = message_handler
        self.message_handler.set_send_function(self.send_message)

        # Try to find the FTDI
        self._ser = []      
        self.open_serial_port()                 
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.setDaemon(True)
        
    def run_in_thread(self):
        """
        Run the app in a thread
        """
        
        self._shutdown = False
        self.run_thread.start()
        return self.run_thread

    def run(self):
       
        while not self._shutdown:
            # look for delimiter
            self.mutex.acquire()

            try:
                #print(' '.join('{:02x}'.format(x) for x in self._ser.readall()))                
                header = self._ser.read(1)                

                if header[0] != BionicMessageBase.get_preamble():                    
                    self.mutex.release()                                        
                    continue
                                
                data = self._ser.read(20)

                if len(data) < 20:
                    print("Wrong data len")
                    self.mutex.release()
                    continue
                
                # Determine length of message
                seq = data[0]  #  Sequence
                length = 0
                try:
                    length = struct.unpack('H', data[1:3])[0]
                except ValueError as e:
                    self.mutex.release()                    
                    logging.error("Error parsing message length : " + str(e))              
                    continue          

                chs = data[3]  # Checksum
                device_id = data[4:19]  # Device id
                
                # read message length
                payload = self._ser.read(length)

                counter = 0
                # handle messages in payload
                while counter < length:
                
                    msg_id = payload[counter]                        
                    msg_length_data = payload[counter + 1:counter + 3]                
                    msg_length = struct.unpack('H', msg_length_data)[0]

                    #print("COUNTER: %d LENGTH: %d" % (counter, length))
                    #print ("ID: %s MSG LENGTH %d" % (msg_id, msg_length))

                    if msg_length <= 0:
                        break                        
                    msg = payload[counter + 2: counter + 2 + msg_length]
                    
                    try:                            
                        self.message_handler.handle_message(msg_id, msg, device_id)                            
                    except Exception as e:                        
                        logging.error(str(e))
                        continue

                    counter += 4 + msg_length                 

                    self.mutex.release()

            except SerialException as e:

                logging.error(f"BIONIC SERIAL CLIENT: {str(e)}")
                self._ser.close()

                self.open_serial_port()
                self.mutex.release()

        self._ser.close()

    def open_serial_port(self):

        serial_port_open = False
        tries = 0
        while not self._shutdown and tries < self._max_retries:
                        
            for port in list_ports.comports():
                logging.info("found: " + str(port.description))

                # TODO: Implement the description finding for Windows
                if self._port in port.description:
                    self._port = port.device                    
                    logging.info("Found suitable Serial device at port: " + str(self._port))
                    try:
                        self._ser = serial.Serial(self._port, self._baud, exclusive=True, timeout=None)                        
                        serial_port_open = True
                        break
                    except SerialException as e:

                        logging.info("But it is already open, continuing our search")
                        logging.error(str(e))

            if not serial_port_open:                
                tries += 1
                logging.error("Could not open any serial port! Retrying in 5 sec (" + str(tries) + "/" + str(self._max_retries) + ")")

                if tries < self._max_retries:
                    time.sleep(5.0)                
            else:
                logging.info("Setting up serial port")
                time.sleep(1.0)                
                break

    def send_message(self, ser_msg):

        logging.info("Sending Message over UART ")
        self.mutex.acquire()
        try:
            # Send bytes
            self._ser.write(ser_msg)            
            # Wait to all bytes are written
            self._ser.flush()            
        except SerialException:
            self.open_serial_port()
        # rospy.sleep(0.020) # time to send
        self.mutex.release()

        return True

if __name__ == "__main__":
    BionicSerialClient()
