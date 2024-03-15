#!/bin/bash

here=`dirname $0`

sudo -u webuser -s nohup $here/run.sh > /tmp/zmq-simple-storage.log 2>&1 &

#if ran from /etc/rc.local it must complete nicely
exit 0