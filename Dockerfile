FROM python:latest
LABEL authors="fraerman"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 23

ENTRYPOINT ["python", "main.py"]