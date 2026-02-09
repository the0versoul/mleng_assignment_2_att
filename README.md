# Assignment 2: Headline Sentiment API

Web service that scores headlines in real time. Uses the model and assets from assignment 1 (sibling folder `mleng_assignment_1_att`).

## Run the service

From this directory (or with `PYTHONPATH` set so it can find the module):

```bash
pip install -r requirements.txt
uvicorn score_headlines_api:app --host 0.0.0.0 --port 8088
```

Or: `python score_headlines_api.py` (runs uvicorn on 8088).

Port 8088 is the one assigned for this student. Make sure nothing else is bound to it (`lsof -i:8088`).

## Endpoints

- **GET /status**  
  Returns `{"status": "OK"}`. Use this to check that the service is up.

- **POST /score_headlines**  
  Body: `{"headlines": ["headline one", "headline two", ...]}`  
  Returns: `{"labels": ["Optimistic", "Neutral", ...]}` (labels only; client matches them to headlines by index).

## Test with curl

```bash
# health check
curl http://localhost:8088/status

# score a few headlines
curl -X POST http://localhost:8088/score_headlines \
  -H "Content-Type: application/json" \
  -d '{"headlines": ["Markets rise on strong jobs report", "Local council delays vote"]}'
```

## Model path

The API looks for `svm.joblib` in `../mleng_assignment_1_att/` by default. Override with env var `HEADLINE_MODEL_PATH` if your layout is different (e.g. on the server).
