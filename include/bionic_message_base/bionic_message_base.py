#!/usr/bin/env python3

__author__ = "Marinus Matthias Moerdijk & Timo Schwarzer"
__copyright__ = "Copyright 2020, Festo Coperate Bionic Projects"
__credits__ = ["Timo Schwarzer", "Marinus Matthias Moerdijk"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.6"
__maintainer__ = "Timo Schwarzer"
__email__ = "timo.schwarzer@festo.com"
__status__ = "Experimental"

import time
import struct
import abc
import logging

class BionicMessageBase:
    """
    All bionic messages should implement this interface
    """
    __metaclass__ = abc.ABCMeta

    last_msg_received_time = -1
    device_id = ""
    raw_msg_data = []
    pointer_pos = 0
    msg_id = 0
    _callback = []
    msg_available = False
    provides = []  # List of sensor ids

    def __init__(self, msg_id):
        self.msg_id = msg_id

        
    def get_id(self):
        return self.msg_id

    def register_cb(self, cb):
        self._callback = cb
        
    @abc.abstractmethod
    def process_msg(self, data, device_id):
        pass
        return

    @staticmethod
    def get_preamble():
        return 0x7E

    # Helper functions

    def get_unique_name(self):
        return str(self.msg_id).replace("BIONIC_MSG_IDS.", "")

    def get_device_id(self):
        return self.device_id

    def print_data(self, data):
        for d in data:
            print('{:02x}'.format(d))

    def set_msg_data(self, data, pointer_pos=0):
        self.last_msg_received_time = int(round(time.time() * 1000))
        self.raw_msg_data = data
        self.pointer_pos = pointer_pos

    def pop_uint32(self, data_size=4, big_endian=False):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 4]
        self.pointer_pos += 4
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)
        res = struct.unpack('I', data)[0]
        return res

    def pop_double_32(self):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 4]
        self.pointer_pos += 4
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)
        res = struct.unpack('f', data)[0]
        return res

    def pop_double_64(self):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 8]
        self.pointer_pos += 8
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)
        res = struct.unpack('d', data)[0]
        return res

    def pop_uint16(self):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 2]
        self.pointer_pos += 2
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)

        res = struct.unpack('H', data)[0]
        return res

    def pop_int16(self):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 2]
        self.pointer_pos += 2
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)

        res = struct.unpack('h', data)[0]
        return res

    def pop_uint8(self):
        data = self.raw_msg_data[self.pointer_pos:self.pointer_pos + 1]
        self.pointer_pos += 1
        # print ">>" + ' '.join('{:02x}'.format(ord(x)) for x in data)

        res = struct.unpack('B', data)[0]
        return res

    def append_bytearray(self, array_to_append, bytes_to_append):
        for b in bytes_to_append:
            array_to_append.append(b)

    def is_msg_available(self):
        tmp = self.msg_available
        self.msg_available = False
        return tmp

    def set_calibration_cb(self, cb):
        self.get_calibration_data = cb

    def apply_calibration(self):
        pass

class BionicActionMessage(BionicMessageBase):
    
    msg = bytearray()

    def __init__(self, sensor_id, action_id, action_values):

        super(BionicActionMessage, self).__init__("BIONIC ACTION ID")

        self.action_values = action_values
        self.sensor_id = sensor_id
        self.action_id = action_id

    def create_message_header(self, length):

        # Create a bionic message 
        # send it with the message handler send function
        self.msg = bytearray()
        # Preamble        
        self.msg.append(self.get_preamble())
        # Sequence
        self.msg.append(1)
        #logging.info("LENGTH: %d", length)
        self.msg.append(length)

        # Checksum TODO: Calculate checksum
        self.msg.append(0xFF)
        # Payload
        self.msg.append(self.sensor_id)
        self.msg.append(self.action_id)

    def create_message_char(self):
        
        # Length + (sensor_id & action_id)
        length = len(self.action_values) + 2

        self.create_message_header(length)

        for action in self.action_values:
            ba = bytearray(struct.pack("B", action))
            for b in ba:
                self.msg.append(b)

    def create_message_short(self):

         # Length + (sensor_id & action_id)
        length = len(self.action_values) * 2 + 2

        self.create_message_header(length)

        for action in self.action_values:
            ba = bytearray(struct.pack("h", action))
            for b in ba:
                self.msg.append(b)

    def create_message_float(self):

        # Length
        length = len(self.action_values) * 4 + 2

        self.create_message_header(length)

        for action in self.action_values:
            ba = bytearray(struct.pack("f", action))
            for b in ba:
                self.msg.append(b)
    
    def process_msg(self, data):

        logging.debug("This should not be called.")

    @property
    def data(self):        
        self.create_message_char()
        return self.msg
