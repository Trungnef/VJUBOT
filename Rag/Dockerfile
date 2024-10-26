FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

COPY . . 
# Expose port cho FastAPI
EXPOSE 8002

# Khởi chạy ứng dụng FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]