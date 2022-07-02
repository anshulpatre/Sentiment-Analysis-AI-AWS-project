FROM python:3.8-alpine
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=server.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]