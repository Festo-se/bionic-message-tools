#!/usr/bin/env python3

__author__ = "Timo Schwarzer"
__copyright__ = "Copyright 2020, Festo Coperate Bionic Projects"
__credits__ = ["Timo Schwarzer"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Timo Schwarzer"
__email__ = "timo.schwarzer@festo.com"
__status__ = "Experimental"

# system imports
import unittest

# custom imports
from bionic_message_tools.bionic_message_tools import BionicMessageHandler
from bionic_message_base.bionic_message_base import BionicMessageBase

class TestBionicMessageTools(unittest.TestCase):

    def setUp(self):
        """
        Setup the unittest 
        """

        self.msg_id = "0x01"
        self.base_msg = BionicMessageBase("0x01")
        self.bionic_message_handler = BionicMessageHandler()        

    def test_registered_msg_count(self):
        """
        Test if it is possible to register a msg with the handler.
        """

        self.bionic_message_handler.register_message_type(self.base_msg)

        msg_count = len(self.bionic_message_handler._messages)
        self.assertEqual(1, msg_count)

    def test_registered_msg_id(self):
        """
        Test if the msg_id is registered
        """

        self.bionic_message_handler.register_message_type(self.base_msg)

        msg_id = self.bionic_message_handler._message_ids[0]
        self.assertEqual(self.msg_id, msg_id)

if __name__ == "__main__":
    unittest.main()