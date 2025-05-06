FROM python:3.10

WORKDIR /app

# Copy API and llm code into container
COPY ./api ./api
COPY ./llm ./llm

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV PYTHONPATH=/app
ENV FLASK_APP=api.main

# Expose port Flask runs on
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
