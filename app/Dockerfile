FROM python:3.11-alpine AS build

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]