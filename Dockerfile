FROM python:3.9-alpine

COPY ./src /app
COPY ./src/config.sample.py /app/config.py
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

#inform of the port to be exposed
EXPOSE 55555

#Create a user to run the application NOT as root
RUN adduser --disabled-password --gecos '' --no-create-home  webuser
USER webuser

#Run the application (-u is to avoid buffering)
CMD ["python", "-u", "zmq-simplestore-server.py"]
