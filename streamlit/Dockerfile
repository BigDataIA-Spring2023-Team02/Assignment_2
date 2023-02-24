# FROM python:3.10.6

# WORKDIR /app

# COPY ./streamlit/Login_Page.py ./streamlit/requirements.txt  /app/
# COPY ./streamlit/pages /app/pages

# RUN pip install -r requirements.txt
# RUN pip install --upgrade pip

# EXPOSE 8501

# CMD ["streamlit", "run", "Login_Page.py"]

FROM python:3.9.12

WORKDIR /app

COPY ./streamlit/Login_Page.py ./streamlit/requirements.txt ./
COPY ./streamlit/pages ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["streamlit", "run", "Login_Page.py", "--server.port", "8000"]