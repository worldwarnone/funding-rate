FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y git && \
    pip install -r requirements.txt

WORKDIR /app

RUN git clone https://github.com/worldwarnone/funding-rate.git

CMD [ "python", "./funding-rate/main.py" ]