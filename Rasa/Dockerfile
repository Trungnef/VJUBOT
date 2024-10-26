FROM rasa/rasa:latest

WORKDIR /app

COPY config.yml credentials.yml domain.yml endpoints.yml data/ /app/

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"] 