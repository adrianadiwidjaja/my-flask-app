# my-flask-app
WHAMO git repo

A minimal Flask application.

## Running locally with Docker

To build and run the application inside a Docker container:

```bash
docker build -t my-flask-app .
docker run -p 5000:5000 my-flask-app
```

The server will start listening on port `5000`, accessible via `http://localhost:5000/`.

