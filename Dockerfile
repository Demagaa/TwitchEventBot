# Use an official MySQL image as the base image
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_DATABASE subscribers
ENV MYSQL_ROOT_PASSWORD root

# Copy the initialization SQL script into the container
COPY /data/application/init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306

# Start the MySQL server when the container starts
CMD ["mysqld"]
