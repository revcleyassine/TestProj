# Use an official Node runtime as a parent image
FROM node:20

# Set work directory
WORKDIR /app/frontend

# Install dependencies
#COPY ./frontend/package.json /app/frontend
#COPY ./frontend/package-lock.json /app/frontend

# Copy project and environment file
COPY ./frontend /app/frontend

# Install dependencies
RUN npm install


RUN chmod +x /app/frontend/entrypoint.sh

# Expose port 5000 for the Vue app
EXPOSE 3000


# Use the entrypoint script
ENTRYPOINT ["/app/frontend/entrypoint.sh"]