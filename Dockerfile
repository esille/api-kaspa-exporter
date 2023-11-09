FROM python:3.12-alpine

ENV KASPA_ADDRESS "kaspa:1,kaspa:2"

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5001/tcp

CMD [ "python", "get_kaspa_balance.py"]