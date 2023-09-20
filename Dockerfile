FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .


# Den Dienst auf Port 5000 starten
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
