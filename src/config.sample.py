import logging
import os

myconfig = {
    "app_port" : int(os.getenv('SERVER_PORT', 55555)),

    "upload folder" : "/tmp/zmq-uploads",

    "logfile" : "/tmp/zmq-logs.log",

    "log level" : logging.INFO,

    "log format" : '%(asctime)s - %(levelname)s - %(message)s'
} 