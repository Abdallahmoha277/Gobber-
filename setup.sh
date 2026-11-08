#!/bin/bash
echo "🚀 Starting Gobber Ultimate Setup..."

# 1. تثبيت أدوات النظام والدوكر
sudo apt-get update
sudo apt-get install -y python3.12-venv docker.io docker-compose

# 2. تجهيز البيئة الافتراضية
python3 -m venv venv
source venv/bin/activate

# 3. تثبيت المكتبات (بما فيها الواجهة)
echo "⏳ Installing dependencies (this takes a few minutes)..."
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
pip install streamlit requests

# 4. تشغيل Docker
echo "🐳 Starting Docker containers..."
sudo systemctl start docker
sudo usermod -aG docker $USER
docker compose up -d

echo "✅ Setup Complete!"
echo "⚠️ IMPORTANT: You MUST create the .env file manually and add your DEEPSEEK_API_KEY before running ./start.sh"
