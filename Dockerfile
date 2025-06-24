# --- Stage 1: Build frontend ---
FROM node:18-alpine AS builder
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY tailwind.config.js ./
COPY static/ ./static/
COPY templates/ ./templates/
RUN npm run css -- --minify

# --- Stage 2: Final Python application ---
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /frontend/static ./static
COPY --from=builder /frontend/templates ./templates
COPY app.py .
COPY sw.js .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 5000
CMD ["./entrypoint.sh"]