FROM python:3.8.12-slim

COPY . /comet/

WORKDIR /comet

RUN pip3 install -r requirements.txt && flask db init && flask init-db && flask forge


EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]