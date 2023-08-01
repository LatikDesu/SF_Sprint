FROM python:3

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
RUN chmod +x entrypoint.sh

EXPOSE 8000

