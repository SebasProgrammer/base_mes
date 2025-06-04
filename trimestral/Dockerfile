FROM python:3.11-slim

COPY config.yml .

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src src
COPY main.py .

CMD ["python", "./main.py"]