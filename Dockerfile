# docker build -t eduardo12543/hangman-streamlit-app .
FROM python:3.10-slim

LABEL version="1.0"
LABEL description="A simple Hangman game using Python."
LABEL maintainer="Eduardo V."
LABEL url="https://github.com/EduardoVparga/hangman-streamlit-app"

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py"]