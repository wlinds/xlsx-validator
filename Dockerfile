FROM python:3.9-slim

WORKDIR /app

COPY src/ /app

RUN mkdir uploads

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]