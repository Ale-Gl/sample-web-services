FROM python:3.6-slim

COPY . .

WORKDIR /root

RUN pip install gunicorn flask_wtf flask joblib numpy sklearn scipy pandas