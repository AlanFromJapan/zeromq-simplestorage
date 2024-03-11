import os
import time
import zmq
import logging
import json
import base64
from config import myconfig


############################ BEFORE ANYTHING ELSE #################################
#logging
logging.basicConfig(filename=myconfig["logfile"], level=myconfig.get("log level", logging.INFO))
logging.info("Starting app")

#make sure upload folder exists
if not os.path.exists(myconfig["upload folder"]):
    os.makedirs(myconfig["upload folder"])

############################ STARTUP OF MQ #################################
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%d" % myconfig["app_port"])

while True:
    #  Wait for next request from client
    msg = socket.recv()
    print("Received request: %s" % msg)

    j = json.loads(msg)
    if j["message"] == "quit":
        #  Send reply back to client
        socket.send_string("BYE")
        print("Shutting down Q")
        break

    if j["message"] == "ping":
        socket.send_string("PONG")
        print("PONG")
        continue

    if j["message"] == "store":
        contents = j["body"]["content"]
        
        print(contents)

        with open(os.path.join(myconfig["upload folder"], os.path.basename(str(j["body"]["filename"]))), "wb") as f:
            f.write(base64.b64decode(contents.encode()))
    
        #  Send reply back to client
        socket.send_string("SAVED")
        print("SAVED")