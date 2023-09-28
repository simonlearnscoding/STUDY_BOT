


# Pull base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip

# Copy project
COPY . . 


# Make the wait-for-it.sh script executable
RUN chmod +x wait-for-it.sh

RUN pip install -r requirements.txt
