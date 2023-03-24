FROM mcr.microsoft.com/playwright:v1.23.0-focal

RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
RUN apt install python3-pip -y

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN npm install -g playwright
RUN playwright install

CMD ["python3", "main.py"]
