FROM python:3.7-alpine

ADD secondary.py /secondary_frst/
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt /secondary_frst/
RUN pip3 install -r secondary_frst/requirements.txt
EXPOSE 6000
COPY . .
WORKDIR /secondary_frst/
