FROM python:3.11-bullseye

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .