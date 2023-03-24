FROM mcr.microsoft.com/playwright/python:v1.32.0-focal

RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
RUN apt install python3-pip -y

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -U playwright
RUN playwright install

CMD ["python3", "main.py"]
