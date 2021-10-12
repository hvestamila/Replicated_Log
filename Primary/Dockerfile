FROM python:3.9-alpine

WORKDIR /Primary

ENV FLASK_APP primary
ENV FLASK_DEBUG 1

RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY *.py .

CMD ["flask", "run"]
