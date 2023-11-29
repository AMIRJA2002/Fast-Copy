# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.11

# Fix python printing
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/

CMD python3 manage.py collectstatic --noinput && \
    gunicorn -b 0.0.0.0:8000 app.wsgi --reload;