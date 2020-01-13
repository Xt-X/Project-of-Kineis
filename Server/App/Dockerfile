# pull official base image
FROM python:3.8.0-alpine

EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install dependencies
RUN apk add --update  \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
    apk add libxslt-dev && \
    pip install  -r requirements.txt

RUN mkdir /server
WORKDIR /server

COPY . /server

ENTRYPOINT ["/server/entrypoint.sh"]

