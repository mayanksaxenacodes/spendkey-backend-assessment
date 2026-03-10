##
# Gunicorn Dockerfile
# See https://pythonspeed.com/articles/gunicorn-in-docker/
FROM python:3.13-slim
WORKDIR /spendkey

ENV PYTHONUNBUFFERED True

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ app/

EXPOSE 3000
CMD [\
    "uvicorn", \
    "--host=0.0.0.0", \
    "--factory", \
    "app.server.factory:create_app", \
    "--port", \
    "3000"\
]
