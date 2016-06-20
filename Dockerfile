FROM python:2.7
ENV ACCESS_TOKEN=xxxxxxxxxx
RUN mkdir /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt --upgrade
RUN chown www-data:www-data -R /code/
USER www-data
ADD . /code/
WORKDIR /code