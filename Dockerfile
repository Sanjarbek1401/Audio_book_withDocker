# Django va Python asosiy image
FROM python:3.9-slim

# Ishchi katalogni o'rnatamiz
WORKDIR /app

# Tizim paketlarini yangilaymiz va espeak o'rnatamiz
RUN apt-get update && apt-get install -y espeak libespeak-ng1

# Talablar faylini nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install -r requirements.txt

# Loyihaning qolgan barcha fayllarini container ichiga nusxalab olamiz
COPY . .

# Django serverini ishga tushiramiz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
