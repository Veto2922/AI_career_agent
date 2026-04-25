#!/bin/bash
# Start the FastAPI server in the background
uv run uvicorn main_api:app --host 0.0.0.0 --port 8000 &

# Start the Gradio app in the foreground
uv run python gradio_app.py
