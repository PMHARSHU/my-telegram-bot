FROM python:3.10-slim

# System updates aur FFmpeg install karna
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app
COPY . /app

# Python packages install karna
RUN pip install --no-cache-dir -r requirements.txt

# Bot run karne ki command
CMD ["python", "bot.py"]
