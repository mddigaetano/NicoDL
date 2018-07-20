# Use an official Python runtime as a parent image
# The Alpine tag uses python3 on alpine linux, with a small footprint
FROM python:alpine

WORKDIR /app

COPY . /app

RUN apk update \
    && apk add ffmpeg

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir Music \
    && mkdir Video

ENTRYPOINT ["python", "NicoNicoLoad.py"]

