FROM ubuntu:latest
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN sudo apt install software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt update
RUN sudo apt install python3.11
RUN python3 -m pip install requirements.txt
RUN python3 ./OnlineTetrisBattleWebsite/manage.py runserver