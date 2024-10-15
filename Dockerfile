# Django va Python asosiy image
FROM python:3.9-slim

WORKDIR /app

# Zaruriy tizim paketlarini o'rnatamiz
RUN apt-get update && apt-get install -y espeak libespeak-ng1 ffmpeg

# Talablar faylini nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihaning qolgan barcha fayllarini container ichiga nusxalaymiz
COPY . .

# entrypoint.sh faylini container ichiga nusxalaymiz va uni bajariladigan fayl qilib belgilaymiz
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# entrypoint.sh faylini ishga tushiramiz
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["gunicorn", "book_audio.wsgi:application", "--bind", "0.0.0.0:8000"]
