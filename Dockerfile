FROM python:3.11-alpine

RUN apk add gcc musl-dev linux-headers

WORKDIR /backend
COPY requirements.txt /backend/.

RUN pip install -r requirements.txt
RUN apk add docker

COPY . /backend/.

CMD ["python3", "./backend/main.py"]