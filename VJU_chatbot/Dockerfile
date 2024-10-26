FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "vjubot_app.py"]