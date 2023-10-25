# Use the official lightweight Python image.
# https://hub.docker.com/_/python

FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt
RUN pip install Flask gunicorn

# Run the web service on container startup.
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 app:app

