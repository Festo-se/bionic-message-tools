#!/usr/bin/env python3

__author__ = "Marinus Matthias Moerdijk & Timo Schwarzer"
__copyright__ = "Copyright 2020, Festo Coperate Bionic Projects"
__credits__ = ["Timo Schwarzer", "Marinus Matthias Moerdijk"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Timo Schwarzer"
__email__ = "timo.schwarzer@festo.com"
__status__ = "Experimental"

import logging
import abc
import platform
import time
import struct
from threading import Thread, Timer, Lock
import subprocess
import socket
from typing import List

from bionic_message_base.bionic_message_base import BionicMessageBase
from bionic_message_tools.bionic_message_tools import BionicMessageHandler

class BionicUdpClient:
    __metaclass__ = abc.ABCMeta

    local_address = 0
    local_port = 0
    remote_address = 0
    remote_port = 0

    receive_thread = []
    message_handler = []
    data_buffer = []

    in_sync = False
    keep_spinning = False

    receive_timer = []

    last_msg_received_time = 0

    send_mutex = Lock()

    def __init__(self, local_address, local_port, remote_address, remote_port, auto_local_address=True,
                 log_level=logging.DEBUG):
        """
        Initialize the udp client.
        """
        self.local_address = local_address
        # Enable debug level logging
        logging.basicConfig(level=log_level)

        # If the local address has to be used automatically

        if auto_local_address:

            # Setup the used ip address on a linux machine
            if platform.system() == "Linux":

                logging.info("Setup ip address on linux.")

                subnet = ".".join(remote_address.split(".")[0:3])
                ips = subprocess.check_output(['hostname', '-I']).split(" ")
                print(ips)
                found = False
                for ip in ips:

                    if subnet in ip:
                        self.local_address = str(ip)
                        logging.info("Setting \"%s\" to local ip" % str(ip))
                        found = True
                        break

                if not found:
                    logging.error("Could not auto determine ip address")
                    self.local_address = local_address

            elif platform.system() == "Windows":

                logging.info("Setup ip address on windows.")
                hostname = socket.gethostname()
                self.local_address = str(socket.gethostbyname(hostname))

            else:
                raise NotImplementedError("Only implemented for linux ")

        else:
            self.local_address = local_address

        logging.info("Using %s as ip" % self.local_address)

        self.local_port = local_port
        self.remote_address = remote_address
        self.remote_port = remote_port

        self.message_handler = BionicMessageHandler()
        self.message_handler.set_send_function = self.send

        self.sock = []

    def start(self):
        """
        Start the receiving task.
        """

        self.keep_spinning = True
        self.receive_timer = Thread(target=self.spin)
        self.receive_timer.start()

    def send(self, data):
        """
        Sending the UDP message
        """
        if type(self.sock) != List:
            self.sock.sendto(data, (self.remote_address, self.remote_port))
        else:
            logging.error("Hand not yet connected.")

    def spin(self):
        """
        The spin function is used as a loop to receive the incoming messages
        """

        logging.info("Binding to socket on port: %s" % str(self.local_port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        server_address_local = (self.local_address, self.local_port)
        try:
            self.sock.bind(server_address_local)
        except Exception as e:
            logging.error(str(e))

        logging.info("Entering receiving loop.")

        while self.keep_spinning:

            data = []

            if not self.in_sync:

                try:

                    data = self.sock.recv(1024)


                    counter=0
                    while self.keep_spinning:

                        # If data found, clear all data before preable
                        if data[counter] == BionicMessageBase.get_preamble():
                            data = data[counter:-1]
                            self.last_msg_received_time = int(round(time.time() * 1000))
                            self.in_sync = True
                            break

                        # If no data found jump out to recieve new data.
                        if counter >= len(data):
                            self.in_sync = False
                            break

                        counter+=1

                except Exception as e:
                    logging.error(str(e))
                    pass

            if self.in_sync:
                # Readout header

                seq = data[1]
                length_data = data[2:4]
                length = struct.unpack('H', length_data)[0]
                #print("SOLL: %s   IST: %s" % (str(length), str(len(data))))
                chs = data[4]

                device_id = ""
                for x in range(16):
                    device_id += chr(data[5 + x])

                # readout message
                payload = data[21:length + 21]
                # self.print_data(payload)

                counter = 0
                # handle messages in payload
                while counter < (length - 5):
                    msg_id = payload[counter]
                    
                    msg_length_data = payload[counter+2:counter+4]
                    msg_length = struct.unpack('H', msg_length_data)[0]

                    #print("COUNTER: %d LENGTH: %d" % (counter, length))
                    #print ("ID: %s MSG LENGTH %d" % (msg_id, msg_length))                    
                                        
                    if msg_length <= 0:                        
                        break

                        # self.print_data(payload[counter+2:counter+2+msg_length])
                    msg = payload[counter + 4:counter + 4 + msg_length]



                    # try:
                    self.message_handler.handle_message(msg_id, msg, device_id)
                    # except Exception as e:
                    #   logging.error("MSG ID: %s MSG LENGTH: %s and ERROR: %s" % (str(msg_id), str(msg_length), str(e)))
                    #     logging.error("message handler error %s" % str(e))

                    counter += 4 + msg_length

                self.in_sync = False

        logging.info("Stopping receiving thread")

    def print_data(self, data, max_length=20):
        """
        Helper function to print the binary data
        """

        logging.debug(' '.join(('{:02x}'.format(d) for d in data[0:max_length]) ))

    def stop(self):
        """
        Stop the udp receiving thread
        """

        self.keep_spinning = False

        try:
            #self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except Exception as e:
            print ("bionic_udp_client (Exception): ", str(e))
            pass
