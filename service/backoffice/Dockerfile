FROM python:3.11-slim AS base

ARG BUILD_DATE

LABEL maintainer="Gopenux" \
      description="Aplicación Flask conectada a MongoDB, Redis y Elasticsearch" \
      buildTime="${BUILD_DATE}" 

RUN apt-get update && apt-get install -y --no-install-recommends \
        tini && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/tini", "--"]

WORKDIR /service/backoffice

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /service/backoffice/app


EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--chdir", "/service/backoffice", "app.app:app"]



