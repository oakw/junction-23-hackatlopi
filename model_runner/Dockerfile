FROM python:3.11-alpine

WORKDIR .
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["runner.py"]

EXPOSE 8765