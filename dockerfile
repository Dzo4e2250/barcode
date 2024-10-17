# Uporabi Python image
FROM python:3.9-slim

# Namesti odvisnosti
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiraj aplikacijo
COPY . /app
WORKDIR /app

# Kopiraj pisavo DejaVuSans.ttf v delovni direktorij
COPY fonts/DejaVuSans.ttf /app/DejaVuSans.ttf

# Zaženi aplikacijo
CMD ["python", "app.py"]
