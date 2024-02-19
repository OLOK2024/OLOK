FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /olok_service

# Set the working directory to /olok_service
WORKDIR /olok_service

# Copy the current directory contents into the container at /olok_service
ADD . /olok_service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt