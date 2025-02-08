FROM python:3.12.4-slim

# Create a new user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory
WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the application directory to the new user
RUN chown -R appuser:appgroup /usr/src/app

# Switch to the new user
USER appuser

EXPOSE 5000

# Set the command to run the application
CMD ["python", "./src/main.py"]