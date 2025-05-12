# FastAPI Mock API


## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Usage

### Running the API

```bash
python -m app.main
```

### Running the API in Docker

Build and start the Docker container:
```bash
docker-compose up --build  # On MacOS: docker compose up --build
```

Stop the Docker container:
```bash
docker-compose down  # On MacOS: docker compose down
```

### Build Docker Image for Deployment in Cloud Run

```bash
docker build -t teambmockapi .
```

Build without cache:
```bash
docker build --no-cache -t teambmockapi .
```

If using Mac with ARM chips
```bash
docker buildx build --platform linux/amd64 -t teambmockapi .
```

Tag the Docker Image
```bash
docker tag teambmockapi australia-southeast2-docker.pkg.dev/team-b-gcp/team-b-mock-api/teambmockapi
```

Push the Image to Artifact Reggistry
```bash
docker push australia-southeast2-docker.pkg.dev/team-b-gcp/team-b-mock-api/teambmockapi
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the tests with:

```bash
pytest
```
