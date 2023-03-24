FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get install -y \
        wget \
        gnupg \
        unzip \
        fonts-noto-color-emoji \
    && wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y \
        google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install selenium

COPY . .

CMD ["python", "main.py"]
