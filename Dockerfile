# Use the official lightweight Python 3.10 image based on Alpine Linux
FROM python:3.10-alpine  

# Set the working directory inside the container to /app
# All subsequent commands (like COPY, RUN, CMD) will be relative to this folder
WORKDIR /app  

# Copy the requirements.txt file into the container at /app/
COPY requirements.txt /app/  

# Upgrade pip (Python’s package installer) and install dependencies from requirements.txt
# --no-cache-dir ensures pip does not save installation cache (keeps image smaller)
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt  

# Copy everything (your source code, config, etc.) from the current directory
# on your host machine into the /app directory inside the container
COPY . /app/  

# Specify the default command to run when the container starts
# CMD runs multiple Python modules sequentially: 
#   1. Initialize the database (config.database)
#   2. Run utility setup tasks (config.utils)
#   3. Start the main application (main.triage_locator)
CMD python3 -m config.database && python3 -m config.utlis && python3 -m main.triage_locator
