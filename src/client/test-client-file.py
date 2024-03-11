#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
# ==> https://zeromq.org/languages/python/

import zmq
import base64

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:55555")


# prepare message
contents = base64.b64encode("Hello World".encode())
contents = str(contents)[2:-1]
msg = """{
    "message": "store",
    "body": {
        "filename": "testfile.txt",
        "content": "%s"
    }
}
""" % contents

print("Sending request %s …" % msg)
socket.send_string(msg)

message = socket.recv()
print(f"Received reply [ {message} ]")


#-------------------------
with open("queue.jpg", "rb") as f:
    contents = base64.b64encode(f.read())
contents = str(contents)[2:-1]
msg = """{
    "message": "store",
    "body": {
        "filename": "q.jpg",
        "content": "%s"
    }
}
""" % contents

print("Sending request %s …" % msg)
socket.send_string(msg)

message = socket.recv()
print(f"Received reply [ {message} ]")
