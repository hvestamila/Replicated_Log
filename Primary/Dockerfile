FROM python:3.7-alpine

ADD primary.py /primary/
ADD message_container.py /primary/
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt /primary/
RUN pip3 install -r primary/requirements.txt
EXPOSE 5000
COPY . .
WORKDIR /primary/
