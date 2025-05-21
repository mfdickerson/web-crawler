# Use the official Python 3.13 image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /src

# Copy requirements and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . .

# Set the default command to run the crawler
CMD ["python", "src/web_crawler.py"]