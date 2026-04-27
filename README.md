# Todo List API

A simple RESTful Todo List API built with Python and Flask.

## Features

- CRUD operations for todo items
- `GET /health` health check endpoint
- In-memory storage (no database required)
- Unit tests with pytest

## Project Structure

```
.
├── app.py              # Flask application and route definitions
├── requirements.txt    # Python dependencies
├── tests/
│   └── test_app.py     # pytest unit tests
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the development server

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

### Run tests

```bash
pytest tests/ -v
```

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/todos` | List all todos |
| POST | `/todos` | Create a todo |
| GET | `/todos/<id>` | Get a todo by id |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

### Examples

```bash
# Health check
curl http://localhost:5000/health

# Create a todo
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# List todos
curl http://localhost:5000/todos

# Mark as done
curl -X PUT http://localhost:5000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a todo
curl -X DELETE http://localhost:5000/todos/1
```
