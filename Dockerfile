# Docker file for the QA Challenge
FROM python:3.8

EXPOSE 8000

RUN mkdir /app
COPY . /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["fastapi", "dev", "/app/application.py", "--host", "0.0.0.0"]
