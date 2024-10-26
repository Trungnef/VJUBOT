FROM python:3.9-slim-buster

WORKDIR /app

# Sao chép các file requirements
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ project
COPY . .

# Tạo thư mục data
RUN mkdir -p data_source/generative_ai

# Expose port cho FastAPI
EXPOSE 8002

# Khởi chạy ứng dụng FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]