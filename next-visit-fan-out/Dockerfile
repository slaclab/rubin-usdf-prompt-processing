FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED True

#ENV PYTHONASYINCIODEBUG 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py"]