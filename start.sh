#!/bin/bash

echo "🚀 Starting Gobber Development Environment..."

if [ ! -d "venv" ]; then
    echo "⚠️ Virtual environment not found. Creating and installing dependencies..."
    python3 -m venv venv
    source venv/bin/activate
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found. Activating..."
    source venv/bin/activate
fi

echo "🐳 Starting Docker containers..."
docker compose up -d

echo "⏳ Waiting for database to be ready..."
sleep 3

echo "🗄️ Running database migrations..."
python -m alembic upgrade head

echo "🌐 Starting FastAPI server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload