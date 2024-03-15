#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
# ==> https://zeromq.org/languages/python/

import os
import sys
import zmq
import base64



MSG_TEMPLATE = """{
    "message": "store",
    "body": {
        "filename": "%s",
        "content": "%s"
    }
}
"""

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55555")

def sendSample():
    # prepare message
    contents = base64.b64encode("Hello World".encode())
    contents = str(contents)[2:-1]
    msg = MSG_TEMPLATE % ("testfile.txt", contents)

    print("Sending request %s …" % msg)
    socket.send_string(msg)

    message = socket.recv()
    print(f"Received reply [ {message} ]")


    #-------------------------
    with open("queue.jpg", "rb") as f:
        contents = base64.b64encode(f.read())
    contents = str(contents)[2:-1]
    msg = MSG_TEMPLATE % ("q.jpg", contents)

    print("Sending request %s …" % msg)
    socket.send_string(msg)

    message = socket.recv()
    print(f"Received reply [ {message} ]")


def sendAny(filepath:str):
    fname = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        contents = base64.b64encode(f.read())
    
    #remove the b' and ' from the string
    contents = str(contents)[2:-1]

    msg = MSG_TEMPLATE % (fname, contents)

    print(f"Storage request of {fname} …")
    socket.send_string(msg)

    message = socket.recv()
    print(f"Received reply [ {message} ]")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sendAny(sys.argv[1])
    else:
        sendSample()