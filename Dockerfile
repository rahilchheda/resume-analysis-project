# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose a port (only needed if you're running a web API like FastAPI/Flask)
EXPOSE 8000

# Command to run the app (adjust this depending on your entry point)
CMD ["python", "main.py"]



COPY Rahil_Chheda_Resume.pdf /app/
