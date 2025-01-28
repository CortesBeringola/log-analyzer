# Python image
FROM python:3.11.9

# Set Working Directory
WORKDIR /cli_app

# Copy the current directory contents into the container
COPY ../.. /cli_app

# Install requirements.txt
COPY ../../requirements.txt requirements.txt

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# In order to execute program directly
ENTRYPOINT ["python", "cli.py"]
