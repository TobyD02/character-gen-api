FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "--port", "80", "--host", "0.0.0.0", "public.index:app"]