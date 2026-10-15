FROM python:3.11-slim

WORKDIR /app

# Cài đặt thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn và tài nguyên game
COPY . .

# Cổng mặc định của Render.com
ENV PORT=10000
EXPOSE 10000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
