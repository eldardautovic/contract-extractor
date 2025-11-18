FROM python:3.11-slim

# Radni direktorij unutar containera
WORKDIR /app

# Kopiranje requirements prije koda radi boljeg cachiranja
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiranje cijele aplikacije
COPY ./ .

# Izlaganje porta
EXPOSE 8000

# Start komanda
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
