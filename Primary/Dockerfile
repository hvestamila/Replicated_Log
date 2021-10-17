FROM python:3.9-alpine

RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++

WORKDIR /Primary

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY *.py .

CMD ["python", "primary.py"]
