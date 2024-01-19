FROM python:3.9
# Use a base image compatible with amd64
FROM amd64/ubuntu:20.04
WORKDIR /app

RUN apt-get update \
    && apt-get install -y python3 \
    && ln -s -f /usr/bin/python3 /usr/bin/python \
    && apt-get install -y python3-pip \
    && ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN pip install bson
RUN pip install flask
RUN pip install pymongo

COPY . .

CMD ["python", "app.py"]
EXPOSE 5009