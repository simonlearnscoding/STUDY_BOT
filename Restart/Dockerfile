# Base image with Python
FROM python:3.9-buster

# Install Node.js
RUN apt-get update -y --fix-missing && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

RUN apt-get update -y --fix-missing && \
    apt-get install -y mariadb-client

# Set work directory in Docker
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY package.json .
COPY ./prisma ./prisma
RUN npm install prisma
RUN npx prisma generate

COPY . .

CMD ["python", "main.py"]



