FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY api /app/api
COPY app /app/app
COPY scripts /app/scripts

RUN python -m pip install --upgrade pip && pip install .

EXPOSE 8501 8000
CMD ["streamlit", "run", "app/Home.py", "--server.address=0.0.0.0", "--server.port=8501"]
