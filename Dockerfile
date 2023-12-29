FROM python:3.11.5-bookworm
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install sqlite3 libsqlite3-dev -y
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]