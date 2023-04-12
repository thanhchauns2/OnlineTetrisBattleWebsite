FROM ubuntu:latest
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install software-properties-common
RUN Y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.11
RUN python3 -m pip install requirements.txt
RUN python3 ./OnlineTetrisBattleWebsite/manage.py runserver