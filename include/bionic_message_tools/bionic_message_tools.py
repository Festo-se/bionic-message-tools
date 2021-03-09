#!/usr/bin/env python3
"""
Provides the functions to work with Bionic Messages
"""

__author__ = "Marinus Matthias Moerdijk & Timo Schwarzer"
__copyright__ = "Copyright 2020, Festo Coperate Bionic Projects"
__credits__ = ["Timo Schwarzer", "Marinus Matthias Moerdijk"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.6"
__maintainer__ = "Timo Schwarzer"
__email__ = "timo.schwarzer@festo.com"
__status__ = "Experimental"

class BionicMessageHandler:
        """
        Message handler for the bionic messages
        Bionic messages should be registered here
        """

        _send_func = []
        _callback_func = []

        def __init__(self):
            self._messages = []
            self._message_ids = []

        def register_message_type(self, msg):
            self._messages.append(msg)
            self._message_ids.append(msg.get_id())

        def register_callback_function(self, callback):            
            self._callback_func = callback

        def set_send_function(self, func):
            self._send_func = func
        
        def send_message(self, data):            
            self._send_func(data)

        def send_messages(self):
            for msg in self._messages:
                if msg.is_msg_available():
                    self._send_func(msg.data)

        def handle_message(self, msg_id, payload, device_id):            
            
            if msg_id in self._message_ids:                                         
                self._messages[self._message_ids.index(msg_id)].process_msg(payload, device_id)               
                return True
            else:
                raise NameError("Unhandled message id: " + '{:02x}'.format(msg_id))
            