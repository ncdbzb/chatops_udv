FROM python:3.11.4

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

WORKDIR /chatops_udv
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /chatops_udv

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000