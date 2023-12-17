FROM python:3.9
MAINTAINER Salman Alkhalifah

RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "wplanner.py"]