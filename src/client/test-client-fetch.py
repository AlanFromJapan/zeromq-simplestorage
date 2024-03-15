#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
# ==> https://zeromq.org/languages/python/

import zmq
import base64
import os
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55555")


# prepare message
msg = """{
    "message": "list"
}
""" 

print("Get files list")
socket.send_string(msg)

message = socket.recv()
print(f"Current files [ {message} ]")



print("Get LATEST FILE")
msg = """{
    "message": "fetch"
}
""" 

socket.send_string(msg)

message = socket.recv_string()
print(f"Current files [ {message} ]")

if str(message) in ("None", "null"):
    print("No file to fetch")
    exit(0)

j = json.loads(message)
#filename storage location, use basename to avoid path traversal
output_filename = os.path.join("testfolder", j["filename"])


with open(output_filename, "wb") as f:
    f.write(base64.b64decode(j["content"].encode()))
