from os import POSIX_FADV_WILLNEED
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
import json
import _thread

#import protocol

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)


class lxSensor:
    def __init__(
        self,
        brokeraddr: str = None,
        port: int = None,
        deviceid: str = None,
        topic: str = None
    ):
        self._brokeraddr = brokeraddr
        self._port = port
        self._deviceid = deviceid
        self._topic = topic
        self._payload = None




    def sub_threading(self):
        try:
            _thread.start_new_thread(self.create_subscriber,(self._topic,))
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@start_new_thread create_subscriber@@@@@@@@@@@@@@@@@@@@@@@")
        except Exception as e:
            logger.info(f"navien start_new_thread error: {e}")


    def create_subscriber(self, topic):
        def on_connect(client, userdata, flags, rc):
            logger.info(f"subscriber_on_cnnect!")
            client.subscribe(topic)
            logger.info(f"create_subscriber topic: {topic}")
            logger.info("on_connect and sub!")

        def on_message(client,userdata,msg):
            self._payload = msg.payload
            logger.info(f"navien sub_on_message! self._payload:{self._payload}")
            #self._pub_client.disconnect()


        self._sub_client = mqtt.Client("subscriber")
        self._sub_client.on_connect = on_connect
        self._sub_client.on_message = on_message
        self._sub_client.connect(self._brokeraddr, self._port)
        #self._client = sub_client
        logger.info("sub_loop_start()")
        self._sub_client.loop_forever()
        



    def publish_once(self,requesttopic,body):
        
        """
        request = {
                "clientId": "98D8630F60FA146E",
                "sessionId": "",
                "requestTopic":"cmd/rc/2/98D8630F60FA146E/remote/did",
                "responseTopic": "cmd/rc/2/98D8630F60FA146E/remote/did/res"
                }
        """
        
        def on_disconnect(client,userdata,flag):
            logger.info("disconnected!!")

        def on_publish(client,userdata,result):
            #time.sleep(5)
            self._pub_client.disconnect()
            logger.info("on_publish!!")

        def on_connect(client,userdata,flag,rc):
            while True:
                    try:
                        logger.info("navienmsg try to publish! topic: {0}, request: {1}".format(self._pubaddr+requesttopic, json.dumps(body)))
                        self._pub_client.publish(topic=self._pubaddr+requesttopic, payload=json.dumps(body))
                        break
                    except Exception as e:
                        print("publish error: ",e)
                        time.sleep(10)
            
            logger.info("on_connect! and pub message")
        
        #self.sub_threading()
        self._pub_client = mqtt.Client("pub")
        self._pub_client.on_connect = on_connect
        self._pub_client.on_publish = on_publish
        self._pub_client.on_disconnect = on_disconnect
        self._pub_client.connect(self._brokeraddr, self._port)
        self._pub_client.loop_forever()
    

if __name__ == '__main__':
    print()
    instance = lxSensor(lxSensor(brokeraddr = '192.168.12.254', port = 1883, topic = IOT/dat/lux, deviceid="lux"))
    instance.create_subscriber(self._topic)
