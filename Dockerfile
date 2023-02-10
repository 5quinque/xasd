# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the python package files into the container
COPY ./setup.cfg .
COPY ./pyproject.toml .

# Install OS dependancies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libmariadb-dev

# We can cache the python dependancies this way
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY ./src ./src

# Install the python package
RUN pip install --no-cache-dir .

# Expose the port that the application will run on
# EXPOSE 8000

# Enable the container to run with hot reloading in dev mode
ENV MODE=dev
ENV PYTHONUNBUFFERED=1

# ENTRYPOINT [ "xasd_uploader", "watch", "/app/watch"]

# CMD [""]

# HEALTHCHECK CMD ps -ef | grep "[x]asd_uploader" || exit 1
