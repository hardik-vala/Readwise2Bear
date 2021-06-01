FROM python:3.9.5-buster

WORKDIR /root/readwise2bear
COPY . /root/readwise2bear
RUN pip install -r requirements.txt
RUN chmod +x /root/readwise2bear/run.sh