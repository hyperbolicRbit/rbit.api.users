#FROM python:3.6.1
FROM python

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install netcat
RUN apt-get update && apt-get install -y netcat

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
ADD . /usr/src/app

# run server
#CMD python manage.py runserver -h 0.0.0.0
CMD ["./entrypoint.sh"]
