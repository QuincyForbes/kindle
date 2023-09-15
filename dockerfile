# Use an official Python runtime as the base image
FROM python:3.11-slim

# Expose the flask port
EXPOSE 5000

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY "./app" ./app
COPY "./user_library" ./user_library
COPY "./requirements.txt" .
COPY "./data.json" .
COPY "./main.py" .

# Install dependencies listed in a requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
