import os
import time
import zmq
import logging
import json
import base64
import datetime
from config import myconfig


############################ CONSTANTS-ish #################################

ACK = "{ \"message\": \"ACK\"}"

############################ BEFORE ANYTHING ELSE #################################
#logging
logging.basicConfig(filename=myconfig["logfile"], level=myconfig.get("log level", logging.INFO))
logging.info("Starting app..")

#make sure upload folder exists
if not os.path.exists(myconfig["upload folder"]):
    os.makedirs(myconfig["upload folder"])

############################ STARTUP OF MQ #################################
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%d" % myconfig["app_port"])

is_running = True

############################ MAIN LOOP #################################
while is_running:
    #  Wait for next request from client
    msg = socket.recv()
    logging.debug ("Received request: %s" % msg)

    j = json.loads(msg)
    if j["message"] == "quit":
        #  Send reply back to client
        socket.send_string(ACK)
        logging.warning("BYE > Shutting down Q")
        is_running = False
        break

    if j["message"] == "ping":
        socket.send_string(ACK)
        logging.info("PONG")
        continue

    if j["message"] == "store":
        contents = j["body"]["content"]

        #add a leading timestamp to the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        #filename storage location, use basename to avoid path traversal
        output_filename = os.path.join(myconfig["upload folder"], timestamp + "_" + os.path.basename(str(j["body"]["filename"])))

        logging.warning(f'Storing file [{j["body"]["filename"]}] as [{output_filename}]')

        with open(output_filename, "wb") as f:
            f.write(base64.b64decode(contents.encode()))
    
        #  Send reply back to client
        socket.send_string(ACK)


logging.info("Application is shutting down.")