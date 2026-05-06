FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Копируем код
COPY . .

# Запускаем через gunicorn + uvicorn workers (продакшен-стандарт)
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]