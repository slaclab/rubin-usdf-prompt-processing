FROM python:3.10-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#CMD [ "python", "main.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app