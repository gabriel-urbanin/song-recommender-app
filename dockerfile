FROM --platform=linux/arm64 python:3.9-slim-bullseye as build

WORKDIR /app

COPY app/ /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p model

EXPOSE 5000

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "5000"]