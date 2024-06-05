# Use an official Python 3.10 runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/backend

# Install dependencies
COPY ./backend/requirements.txt /app/backend
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Copy project and environment file
#COPY ./ /app/backend
RUN ls -l /app && if [ -x "$(command -v tree)" ]; then tree /app; fi
COPY .env /app/
COPY ./backend/entrypoint.sh /app/backend

# Ensure the entrypoint script is executable
RUN chmod +x /app/backend/entrypoint.sh

# Expose port 8000 for the Django app
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/backend/entrypoint.sh"]
