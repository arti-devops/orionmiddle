# Specify the base image
FROM python:3.9

# Install dependencies required for building Python packages
RUN apk add --no-cache build-base python3-dev py3-pip

# Create and set the working directory
WORKDIR /app

# Copy the Node.js application code to the working directory
COPY orionmiddle .

# Install Node.js dependencies
RUN pip install uvicorn
RUN pip install requests
RUN pip install pandas
RUN pip install fastapi
# Expose the port the app listens on
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
