FROM python:3.11-alpine
LABEL maintainer="yaroslavdidkivskiy@gmail.com"

ENV PYTHONUNBUFFERED 1

# Use absolute path for WORKDIR
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

# Create media directory with correct permissions
RUN mkdir -p /files/media && \
    adduser --disabled-password --no-create-home my_user && \
    chown -R my_user:my_user /files/media && \
    chmod -R 755 /files/media

USER my_user