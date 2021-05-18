FROM python:3.9-alpine

ADD . /opt/rallyapp
WORKDIR /opt/rallyapp

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev gcc gfortran openblas-dev lapack-dev cython

RUN pip install -r requirements.txt

CMD ["python", "app.py"]