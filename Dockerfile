FROM python:2.7
ENV ACCESS_TOKEN=EAAIa0FMrYZBoBANSZAqPQvlnG0fYD6Y93YIdwFhcKBL8IV3QaDiCah6EyW6Lsa381n0ZBc2pDAoXsrkV3jWbLny4Uny1R3bi4cK5TYD480ZAYwHRMerpAIS70C2S9QfGTz8L5pe2Oo66BnZBKUOmU4uI1qIaJLPHYLBmgHqSZCOQZDZD
RUN mkdir /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt --upgrade
RUN chown www-data:www-data -R /code/
USER www-data
ADD . /code/
WORKDIR /code