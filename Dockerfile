FROM python:3.13


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


# Create data directory
RUN mkdir -p data logs

COPY ./data/resources.csv data

COPY ./data/sample-ereserve-data.json data

# Set environment variables
ENV APP_NAME="Mock API"
ENV APP_VERSION="0.1.0"
ENV APP_DESCRIPTION="Mock API using FastAPI - Team B"
ENV CSV_FILE_PATH="data/resources.csv"
ENV JSON_FILE_PATH="data/sample-ereserve-data.json"
ENV LOG_LEVEL="INFO"
ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES="60"

# Set the value of SECRET_KEY securely on serve side

# Use the PORT environment variable with fallback to 8000
ENV PORT=${PORT:-8000}

# Expose port
EXPOSE ${PORT}

# Command to run the application
# Use when using docker compose
# CMD ["uvicorn", "app.main:root_app", "--host", "0.0.0.0", "--port", "8080"]

# Use when using docker build
CMD ["sh", "-c", "uvicorn app.main:root_app --host 0.0.0.0 --port ${PORT}"]