import os
import time
import zmq
import logging
import json
import base64
import datetime
import re
from config import myconfig


############################ CONSTANTS-ish #################################

MSG_ACK = "{ \"message\": \"ACK\"}"
MSG_FETCH = "{ \"filename\": \"%s\", \"content\": \"%s\"}"
RE_LISTFILTER = re.compile(r'^[0-9]{20}_.*')

############################ BEFORE ANYTHING ELSE #################################
#logging
logging.basicConfig(filename=myconfig["logfile"], level=myconfig.get("log level", logging.INFO), format=myconfig.get("log format", '%(asctime)s - %(levelname)s - %(message)s'))
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
def list_files():
    files = os.listdir(myconfig["upload folder"])
    files = [x for x in files if RE_LISTFILTER.match(x)]
    files.sort()
    files.reverse()
    return files

############################ MAIN LOOP #################################
while is_running:
    #  Wait for next request from client
    msg = socket.recv()
    logging.debug ("Received request: %s" % msg)

    j = json.loads(msg)
    if j["message"] == "quit":
        #  Send reply back to client
        socket.send_string(MSG_ACK)
        logging.warning("BYE > Shutting down Q")
        is_running = False
        break

    if j["message"] == "ping":
        socket.send_string(MSG_ACK)
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
        socket.send_string(MSG_ACK)
    
    if j["message"] == "list":
        #returns the list of properly uploaded files, latest first
        files = list_files()
        socket.send_string(json.dumps(files))   

    if j["message"] == "fetch":
        #returns the latest uploaded file or None if nothing is there
        files = list_files()
        if files is None or len(files) == 0:
            socket.send_string("None")
        else:
            #send the file
            with open(os.path.join(myconfig["upload folder"], files[0]), "rb") as f:
                msg = MSG_FETCH % (files[0], base64.b64encode(f.read()).decode())
                socket.send_string(msg)
            #delete the file after it has been fetched
            os.remove(os.path.join(myconfig["upload folder"], files[0]))

logging.info("Application is shutting down.")