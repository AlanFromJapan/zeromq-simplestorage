#!/bin/bash


here=`dirname $0`
cd $here

/bin/bash -c "source bin/activate ; cd src; python zmq-simplestore-server.py"
