FROM python:3

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your app runs on (change if needed)
EXPOSE 8000

# Define the command to run your app (update accordingly)
CMD ["python", "app.py"]
