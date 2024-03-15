# zeromq-simplestorage
A simple storage service to store and retrieve files with ZeroMQ. **No security at all, don't use outside home NW!**
I use it to push/pop files between services asynchonously within my home NW.

But if you have __within your home NW__, a need for a simple & anonymous storage-retrieve service, that should do the trick.

ZeroMQ ==> https://zeromq.org/languages/python/

# Install
git clone https://github.com/AlanFromJapan/zeromq-simplestorage.git
cd zeromq-simplestorage
cp config.sample.py config.py
#edit config to your heart content...
python3 -m venv .
source bin/activate
python -m pip install -r requirements.txt

# Run
## Manually
source bin/activate
cd src/
python zmq-simplestore-server.py

## As a pseudo-service

Add to your /etc/rc.local a call to start-service.sh