import zmq
import config
import os
import base64

__MSG_PING = """{
    "message": "ping"
}
""" 

__MSG_LIST = """{
    "message": "list"
}
""" 

__MSG_STORE = """{
    "message": "store",
    "body": {
        "filename": "%s",
        "content": "%s"
    }
}
"""

__MSG_FETCH = """{
    "message": "fetch"
}
""" 

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect(config.config["zmq_server"])


def ping():
    print("Sending request %s …" % __MSG_PING)
    socket.send_string(__MSG_PING)
    message = socket.recv()
    print(f"Received reply [ {message} ]")
    return str(message)[2:-1]



def list():
    print("Sending request %s …" % __MSG_LIST)
    socket.send_string(__MSG_LIST)
    message = socket.recv()
    print(f"Received reply [ {message} ]")
    return str(message)[2:-1]


def storeFile(filename:str):
    fname = os.path.basename(filename)

    with open(filename, "rb") as f:
        contents = base64.b64encode(f.read())
    
    #remove the b' and ' from the string
    contents = str(contents)[2:-1]

    msg = __MSG_STORE % (fname, contents)

    print(f"Storage request of {fname} …")
    socket.send_string(msg)

    message = socket.recv()
    print(f"Received reply [ {message} ]")
    return str(message)[2:-1]



def dropHead():
    print("Sending request %s …" % __MSG_FETCH)
    socket.send_string(__MSG_FETCH)
    message = socket.recv()
    print(f"Received reply [ {message} ]")
    return "Done."   