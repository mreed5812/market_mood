# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install Flask and other dependencies
RUN pip install Flask

# Copy the application files into the container
COPY . /app

# Command to run the application
CMD ["python", "src/app.py"]
