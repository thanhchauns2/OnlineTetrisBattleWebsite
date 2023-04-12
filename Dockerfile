FROM ubuntu:latest
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python3 -m pip install requirements.txt
RUN python3 ./OnlineTetrisBattleWebsite/manage.py runserver