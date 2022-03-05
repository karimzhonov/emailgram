FROM python:3.9

RUN apt update && apt install postgresql -y

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
