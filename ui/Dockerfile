FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD streamlit run news.py --server.address=0.0.0.0 --server.port=8501
