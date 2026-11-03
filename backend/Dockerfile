FROM python:3.13-slim

WORKDIR /app

# the mariadb Python package compiles against MariaDB Connector/C
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
