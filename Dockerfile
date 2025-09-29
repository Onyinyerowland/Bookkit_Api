# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set work directory
WORKDIR /app

# 4️⃣ Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy project files
COPY . .

# 7️⃣ Expose port
EXPOSE 8000

# 8️⃣ Run the app with uvicorn
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

# If you want to use the factory function, change it back to "app.main:create_app"
# and ensure that the function is correctly defined to return the FastAPI instance.
# Also, added --reload for development purposes; remove it for production.
# Make sure to adjust the command based on your actual application structure and needs.
# For production, consider using a production server like Gunicorn with Uvicorn workers.
# Example for production:
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker",
#      "app.main:app", "--bind", "
#      "
