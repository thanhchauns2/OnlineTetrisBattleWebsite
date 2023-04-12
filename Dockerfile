FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.11 -y
RUN apt-get install python3-pip -y
RUN python3 -m pip install -r ./requirements.txt
RUN python3 ./manage.py runserver