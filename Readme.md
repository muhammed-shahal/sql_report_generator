# Create Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
```

# Install Requirements
```sh
pip install -r requirements.txt
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

# Create DB

```sh
docker compose up
```

# Insert Data

```sh
python3 scripts/bulk_data_loader.py
```

Docs: http://127.0.0.1:8000/docs

# Install LLM

```sh
ollama run llama3
```

# Run Backend

```sh
uvicorn backend.app:app --reload
```

# Run Front End

```sh
streamlit run frontend/app.py
```