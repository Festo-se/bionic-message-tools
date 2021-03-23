#! /usr/bin/env python3

import logging
import time
import threading
import paho.mqtt.client as mqtt

class BionicMqttClient:
    
    publishers = []
    subscribers = []
    isShutdown = False

    def __init__(self, url, msg_cb, port=1883):
        """
        The BionicMqttClient handles the setup to connect with a broker
        Provide the url and the Message callback function which is called when a
        subscribed topic receives a new message.        
        """
        logging.basicConfig(level=logging.INFO)

        self.msg_cb = msg_cb
        self.port = port
        self.url = url
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe        

        self.thread = threading.Thread(target=self.run)
        
    def run_in_thread(self):

        self.thread.start()

    def add_subscriber(self, topic, qos=2):

        self.subscribers.append(topic)        

    def run(self):

        self.mqttc.connect(self.url, self.port, 60)
        self.mqttc.loop_forever()     

    def shutdown(self):

        self.isShutdown = True    
        self.mqttc.loop_stop()                 
        self.mqttc.disconnect()
        
    def publish(self, topic, msg, qos=2):

        logging.debug(f"Published msg: \"{msg} \"on topic: {topic}")
        pub = self.mqttc.publish(topic, msg, qos=qos)
        pub.wait_for_publish()
    
    def on_connect(self, mqttc, obj, flags, rc):
        logging.debug("rc: " + str(rc))
        
        for x in self.subscribers:
            self.mqttc.subscribe(x, qos=2)

    def on_message(self, mqttc, obj, msg):    
        """
        QOS: Quality of servive: 0 = max once; 1 = at least once; 2 = exactly once
        """
        logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))    

        try:            
            self.msg_cb(msg)
        except Exception as e:
            logging.error(str(e))

    def on_publish(self, mqttc, obj, mid):
        logging.debug("mid: " + str(mid))
        pass

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logging.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        logging.debug(string)
