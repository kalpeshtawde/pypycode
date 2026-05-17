# Vega

Vega is the AI agent service for PyPyCode. Given a user's natural language goal (e.g. *"I have a coding interview in 2 weeks"*), it analyses the user's past performance, selects a strategy, and generates a personalised problem set that is persisted as a project on the backend.

Vega runs as a standalone Flask microservice and is called by the main backend over HTTP.

---

## How It Works

### High-Level Flow

```
Backend (Flask)
  POST /projects/from-prompt
    │
    ├─ mints a short-lived JWT for the calling user
    └─ calls → POST http://vega:5001/generate
                  │
                  └─ LangGraph agent runs
                       └─ persists project via backend API
                            └─ returns project to backend
```

### Agent Graph

The LangGraph graph runs the following nodes in order:

```
START
  └─ fetch_user_stats          # GET user's difficulty stats from backend
       └─ classify_user_level  # beginner / intermediate / advanced
            └─ fetch_user_tag_stats   # GET per-tag weakness scores
                 └─ pick_strategy     # LLM picks: warmup | weakness_fix | topic_focus | revision | mixed
                      └─ build_distribution          # difficulty % split
                           └─ convert_distribution_to_counts  # % → counts
                                └─ select_problems    # POST /problems/select
                                     └─ should_retry_selection  ──retry──> adjust_inputs ─┐
                                          │ good / give_up                                 │
                                          └─ assemble_project                              │
                                               └─ explain_project  (LLM explanation)       │
                                                    └─ persist_project  (POST /projects/)  │
                                                         └─ END  <───────────────────────-─┘
```

### Strategies

| Strategy | When chosen | Behaviour |
|---|---|---|
| `warmup` | New user, returning after break, or goal mentions "easy" | All-easy problem set |
| `weakness_fix` | Goal mentions weak areas / interview, and tag stats show real weaknesses | Heavily weights weakest tags |
| `topic_focus` | Goal names specific topics (e.g. "DP", "graphs") | Equal weight on named tags only |
| `revision` | Goal mentions "review" or "revise" | Balanced over weak tags with exploration |
| `mixed` | Default | Balanced across difficulties and tags |

---

## Project Structure

```
vega/
├── vega_service.py        # Flask app — entry point, exposes /health and /generate
├── agent/
│   ├── nodes.py           # All LangGraph nodes + graph definition
│   ├── state.py           # AgentState TypedDict
│   └── strategies.py      # Strategy builders (warmup, weakness_fix, etc.)
├── clients.py             # BackendClient — async HTTP client for the backend API
├── schemas.py             # Pydantic request/response models
├── constants.py           # Runtime configuration (reads from env vars)
├── enums.py               # UserLevel enum
├── problem_set_generator.py  # Level classification logic
├── requirements.txt
└── Dockerfile
```

---

## API Endpoints

### `GET /health`
Returns `{"status": "healthy"}`. Used by Docker healthchecks.

### `POST /generate`
Invokes the LangGraph agent and returns the generated project.

**Request body:**
```json
{
  "prompt": "I have a coding interview in 2 weeks",
  "problem_count": 20,
  "auth_token": "<JWT issued by the backend for the calling user>",
  "user_id": "<user UUID>"
}
```

**Response:** Full `AgentState` after graph completion, including `project` and `project_id`.

---

## Environment Variables

### Production

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | **Yes** | — | OpenAI API key used by the LangGraph LLM nodes |
| `VEGA_BACKEND_BASE_URL` | No | `http://localhost:81` | Base URL of the PyPyCode backend API |
| `LANGCHAIN_API_KEY` | No | — | LangSmith API key for tracing (optional) |
| `LANGCHAIN_TRACING_V2` | No | — | Set to `true` to enable LangSmith tracing |

### Local Dev Only

| Variable | Description |
|---|---|
| `VEGA_AUTH_TOKEN` | Fallback JWT for running `nodes.py` directly as a script. In production the backend always passes a per-request JWT in the request body — this variable is never read. |
| `VEGA_USER_ID` | Fallback user ID for the `main()` entry point in `nodes.py`. In production the `user_id` always comes from the request body — this variable is never read. |

---

## Running Locally

### Prerequisites
- Python 3.12+
- The PyPyCode backend running and accessible (default: `http://localhost:81`)
- An OpenAI API key

### Setup

```bash
cd vega
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment

Create a `.env` file or export variables:

```bash
export OPENAI_API_KEY=sk-...
export VEGA_BACKEND_BASE_URL=http://localhost:81

# Only needed for running agent/nodes.py directly as a script
export VEGA_USER_ID=<your-user-uuid>
export VEGA_AUTH_TOKEN=<a-valid-jwt-from-the-backend>
```

### Start the service

```bash
flask --app vega_service run --host=0.0.0.0 --port=5001
```

Or with gunicorn (matches the Docker setup):

```bash
gunicorn -w 1 -b 0.0.0.0:5001 vega_service:app
```

### Test it

```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I want to practice dynamic programming",
    "problem_count": 10,
    "auth_token": "<JWT>",
    "user_id": "<user-uuid>"
  }'
```

---

## Running with Docker

The service is built and started as part of the main `docker-compose` setup. To build and run in isolation:

```bash
docker build -t vega .
docker run -p 5001:5001 \
  -e OPENAI_API_KEY=sk-... \
  -e VEGA_BACKEND_BASE_URL=http://host.docker.internal:81 \
  vega
```
