# Headline Sentiment API (Assignment 2)

Small web service that scores headlines with the same sentiment model from assignment 1. Two endpoints: a health check and a POST that takes a list of headlines and returns labels only.

## Running it

The API looks for the model file `svm.joblib` in the same folder as `score_headlines_api.py` (relative path, so it works the same locally and on the server). The file is in `.gitignore` so it’s not in the repo—if you’re deploying somewhere, copy `svm.joblib` into this folder first (e.g. with scp). You can override with `HEADLINE_MODEL_PATH` if you need to point somewhere else.

```bash
pip install -r requirements.txt
uvicorn score_headlines_api:app --host 0.0.0.0 --port 8088
```

Use port **8088** (assigned for alextsourmas). Same port on the server. First startup can take a bit while the transformer model loads.

## Endpoints

**GET /status**

Returns `{"status": "OK"}` so you can check the service is up.

```bash
curl http://localhost:8088/status
```

**POST /score_headlines**

Send a JSON body with a list of headlines. You get back a list of labels in the same order (Optimistic, Neutral, or Pessimistic). No headline text in the response so the client has to match by index if needed.

Request body:
```json
{"headlines": ["First headline here", "Second one", "etc"]}
```

Response:
```json
{"labels": ["Optimistic", "Neutral", "Pessimistic"]}
```

Example with curl:

```bash
curl -X POST http://localhost:8088/score_headlines \
  -H "Content-Type: application/json" \
  -d '{"headlines": ["Markets rise on jobs data", "City council delays vote"]}'
```

That’s it. The model and transformer are loaded once at startup, not per request.
