# Use the official Python 3.13 image
FROM python:3.13-slim

# Set working directory in the container
WORKDIR /app


# Copy project files into the container
COPY . /app

# Install requirements for running the module
RUN pip install --no-cache-dir -r src/requirements/dev.txt

# Set the default command to run the crawler using __main__.py
ENTRYPOINT ["python", "-m", "src.web_crawler"]