# Create Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

# Create DB

```sh
docker compose up
```

# Insert Data

```sh
python3 scripts/bulk_data_loader.py
```

# Run App

```sh
uvicorn backend.app:app --reload
```

Docs: http://127.0.0.1:8000/docs

# Install LLM

```sh
ollama run llama3
```