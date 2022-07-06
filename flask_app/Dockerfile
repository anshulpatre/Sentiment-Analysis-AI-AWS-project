FROM python:3.7-alpine
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r req.txt
RUN python -c "import nltk; nltk.download('vader_lexicon')"
ENV FLASK_APP=server.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]