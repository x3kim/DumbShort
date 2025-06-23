# --- Stage 1: Build frontend ---
# We use a Node image to compile our CSS file
FROM node:18-alpine AS builder
WORKDIR /frontend

# Copy the package files and install node modules
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend files
COPY tailwind.config.js ./
COPY static/ ./static/
COPY templates/ ./templates/

# Build the final CSS file
RUN npm run css -- --minify


# --- Stage 2: Final Python application ---
# We start with a slim Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend assets from the first stage
COPY --from=builder /frontend/static ./static
COPY --from=builder /frontend/templates ./templates

# Copy the rest of the app (app.py, sw.js, etc.)
COPY app.py .
COPY sw.js .
# The DB file is not copied, it will be mounted as a volume

# Expose the port Gunicorn will listen on
EXPOSE 5000

# The command to start the application when the container runs
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]