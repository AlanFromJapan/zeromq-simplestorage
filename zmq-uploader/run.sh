#!/bin/bash


here=`dirname $0`
cd $here

/bin/bash -c "source ../bin/activate ; cd zqm-uploader; python zmq-uploader.py"
