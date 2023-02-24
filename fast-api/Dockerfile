FROM python:3.10.6

RUN pip install --upgrade pip

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8080", "main:app"]