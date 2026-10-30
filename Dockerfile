FROM python:3.11-slim AS builder

# psycopg[c] compiles against the PostgreSQL client library, so this stage
# needs a C compiler and the libpq headers. Neither is installed in the 
# final image.
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.12.11

WORKDIR /app
COPY requirements.txt ./

# requirements.txt names psycopg[binary], the prebuilt package used for local
# development. The image uses psycopg[c], built from source, at the same
# pinned version
RUN sed 's/^psycopg\[binary\]==/psycopg[c]==/' requirements.txt > requirements-container.txt \
 && uv venv --python 3.11 /app/.venv \
 && uv pip install --python /app/.venv/bin/python -r requirements-container.txt


# Stage 2 builds the final image, which is based on the same slim Python image but
# does not include the build tools or PostgreSQL headers. It copies the virtual
FROM python:3.11-slim

# libpq5 is the PostgreSQL client library psycopg needs at run time. The
# compiler from the build stage are deliberately absent.
RUN apt-get update \
 && apt-get install --no-install-recommends -y libpq5 \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 app

WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY --chown=app:app alembic.ini ./
COPY --chown=app:app alembic ./alembic
COPY --chown=app:app app ./app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]