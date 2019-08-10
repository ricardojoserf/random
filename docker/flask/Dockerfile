FROM python:2.7
RUN mkdir /test
WORKDIR /test
ADD requirements.txt /test/
RUN pip install -r requirements.txt
COPY app.py /test/
EXPOSE 5000

