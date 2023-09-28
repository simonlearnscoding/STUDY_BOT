#!/bin/bash

# Set the MySQL host and port
HOST='db'  # the service name in docker-compose.yml
PORT=3306

echo "Waiting for MySQL ($HOST:$PORT) to start..."
while ! nc -z $HOST $PORT; do
  sleep 0.1
done

echo "MySQL is up and running!"

# Run the migrations
echo "Running migrations..."
python manage.py migrate

# Now run your application
exec "$@"
