FROM python:3.11-alpine

WORKDIR /usr/src

COPY requirements.txt *.py .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python -B backend.py