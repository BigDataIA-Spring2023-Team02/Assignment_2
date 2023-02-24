FROM python:3.10.6

RUN pip install --upgrade pip

WORKDIR /app

COPY apimain.py ../requirements.txt ../user_data.db /app/

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "apimain:app", "--reload", "--port", "8080:8080"]
# CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8000", "apimain:app"]