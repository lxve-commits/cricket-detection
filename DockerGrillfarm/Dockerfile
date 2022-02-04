FROM python:3.7.10

COPY requirements /

RUN pip install -r /requirements

RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'

COPY grillfarm /

COPY ./commands.sh /

RUN chmod +x /commands.sh

COPY trained_model /trained_model

RUN apt update 

