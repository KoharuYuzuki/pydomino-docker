FROM --platform=linux/amd64 ubuntu:24.04

RUN apt update -y
RUN apt upgrade -y

RUN apt install -y python3-dev pip cmake git
RUN apt install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001

RUN git clone --recursive https://github.com/DwangoMediaVillage/pydomino.git
RUN cd pydomino && pip install ./ --break-system-packages

RUN pip install librosa --break-system-packages

WORKDIR /workspace
