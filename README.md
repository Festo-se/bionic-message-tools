[![FESTO](images/logo.png)](https://www.festo.com/group/de/cms/10156.htm)

> <p style="font-size:30px">BIONIC MESSAGE TOOLS </p>

<br></br>

# LICENSE
The Festo BionicMessageTools are published under the [GNU GPL v3.0 License](https://www.gnu.org/licenses/gpl-3.0.de.html).

# PURPOSE
These tools were developed to enable a bidirectional communication with our hardware.
Currently they are used for the BionicSoftHand Project. It is possible to talk to the Hand with the UDP implementation.     
The serial communication is only for a specific sensor to test them independent from the other hardware.

# USING WITH THE BIONIC SOFT HAND 
If this package is used within the BionicSoftHand project, please refer either to the BionicSoftHand [python](https://github.com/Schwimo/phand-python-libs/blob/master/README.md) or [ROS](https://github.com/Schwimo/phand-ros/blob/master/README.md) install instructions.

# INSTALL INSTRUCTIONS 
```
pip3 install . 
```
to install this library locally on your computer.

# CREDITS:
This project uses the following libraries:
- [PySerial](https://pypi.org/project/pyserial/) which is published under the BSD license