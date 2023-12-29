FROM python:3.10-slim-bullseye
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get upgrade
RUN apt-get install sqlite3 libsqlite3-dev -y
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]