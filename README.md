# Open Innovation AI QA Challenge

This project contains the files for the Open Innovation AI QA challenge.

## Start the server

The challenge provides a test server that exposes the API.

The server listens for connections on port 8080.

### Docker

To start the server run:

```shell
docker-compose up
```

To stop the server run:

```shell
docker-compose down
```

### Manually

It is also possible to run the server manually.

It is recommended to use a virtual environment.

Install the requirements with

```shell
pip install -r requirements.txt
```

The run the server with

```shell
fastapi dev application.py
```

## API Documentation

After starting the server the documentation can be checked at http://localhost:8000/docs

The API documentation can also be found in `docs/openapi.json`.

## Sample Requests

### Add Model

Endpoint: `POST /model`

```json
{
  "name": "My Model",
  "owner": "john"
}
```

### Add Model Version

Endpoint: `POST /model/{model_id}/versions`

```json
{
  "name": "Version 1 - Tiny Llama",
  "hugging_face_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
}
```

### Perform Inference

Endpoint: `POST /model/{model_id}/versions/{version_id}/infer`

```json
{
  "text": "Hi, how are you?"
}
```