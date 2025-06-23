# --- Stufe 1: Frontend bauen ---
# Wir benutzen ein Node-Image, um unsere CSS-Datei zu kompilieren
FROM node:18-alpine as builder
WORKDIR /frontend

# Kopiere die package-Dateien und installiere die Node-Module
COPY package*.json ./
RUN npm install

# Kopiere den Rest der Frontend-Dateien
COPY tailwind.config.js ./
COPY static/ ./static/
COPY templates/ ./templates/

# Baue die finale CSS-Datei
RUN npm run css -- --minify


# --- Stufe 2: Finale Python-Anwendung ---
# Wir starten mit einem schlanken Python-Image
FROM python:3.11-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Python-Abhängigkeiten
COPY requirements.txt .

# Installiere die Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere die gebauten Frontend-Assets von der ersten Stufe
COPY --from=builder /frontend/static ./static
COPY --from=builder /frontend/templates ./templates

# Kopiere den Rest der App (app.py, sw.js etc.)
COPY app.py .
COPY sw.js .
# Die DB-Datei wird nicht kopiert, sie wird als Volume gemountet

# Gib den Port frei, auf dem Gunicorn lauschen wird
EXPOSE 5000

# Der Befehl, um die Anwendung zu starten, wenn der Container läuft
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]