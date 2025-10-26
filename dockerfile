FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/main.py"]
#CMD ["python", "test_db.py"]
#CMD ["python", "/app/app/db/db_postgress.py"]