# Base image with Python and Node.js
FROM nikolaik/python-nodejs:python3.9-nodejs14

RUN apt-get update && \
    apt-get install -y default-mysql-client
# Set work directory in Docker
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Prisma and generate Prisma client
COPY package.json .
COPY ./prisma ./prisma
RUN npm install prisma
RUN npx prisma generate

# Copy the rest of the application
COPY . .

# Run the Python script
CMD ["python", "main.py"]
