# Django va Python asosiy image
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y espeak libespeak-ng1 ffmpeg

# Talablar faylini nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihaning qolgan barcha fayllarini container ichiga nusxalab olamiz
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY . .
CMD ["entrypoint.sh"]