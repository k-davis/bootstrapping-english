FROM python:3.9-bookworm

RUN apt-get update 
RUN pip install --upgrade pip
RUN pip install ipykernel
RUN pip install graphbrain
RUN python -m spacy download en_core_web_trf
RUN pip install pywsd