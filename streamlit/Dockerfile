FROM python:3.10.6

WORKDIR /app

COPY Login_Page.py req.txt ./

COPY ./streamlit/Login_Page.py ./streamlit/requirements.txt  /app/
COPY ./streamlit/pages /app/pages
COPY ./jwt_fastapi.py /app/

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

EXPOSE 8601

CMD ["streamlit", "run", "main.py", "--server.port", "8601"]