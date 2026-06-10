FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# Command to run the application
# CMD ["python", "app.py"]
# Using gunicorn for better production-like behavior, but it might not be installed by default if not in requirements.txt
# If gunicorn is not in requirements.txt, it will fail. Let's stick to python app.py for simplicity for now.
CMD ["python", "app.py"]
