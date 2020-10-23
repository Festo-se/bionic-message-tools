=======================
 BIONIC SOFT HAND 2.0
=======================

.. warning::
    The maximum allowed pressure is 5 Bars. If you provide more than this, the hand will get damaged.

.. image:: images/logo.png
    :align: left

The BionicSoftHand is a pneumatic actuated robot hand. 
It has felexible structures and uses elastic materials and ligthweight components.
With its integrated valve terminal the BionicSoftHand is able to control 12 independent degrees of freedom.
Two are used for the wrist and the other 10 for the fingers. 

Each finger consists of two chambers. The lower (L) one and an upper (U) one.
The thumb and the index finger have also the possibility to move lateral.
How the DoFs are allocated is noted in the list below.

.. list-table:: Degrees of Freedom
   :widths: 25 10  65
   :header-rows: 1

   * - Name
     - Amount
     - Description     
   * - Thumb
     - 3
     - Side, Lower, Upper     
   * - Index
     - 3
     - Side, Lower, Upper     
   * - Middle
     - 2
     - Lower (Connected with Ring), Upper (Connected with Ring)
   * - Ring
     - 2
     - Lower (Connected with Middle), Upper (Connected with Middle)
   * - Pinky
     - 1
     - Combined

The BionicSoftHand needs one tube for air supply, one cable for 24V power supply and an ethernet connection.
It provides bidirectional communication to readout sensor values or set parameters (e.g. pressure values to actuate the fingers).
How to send and receive data between host and hand is explained in the following sections.


