# Dockerfile for production application


# Use official python docker base image
FROM python:3.8-slim

# Set the default working directory of the project on the container
WORKDIR /app

# Copy the requirements.txt file over to the container. 
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Install production WSGI server
RUN pip install gunicorn[gevent]

# Install the project on the container.
COPY . .

# Configure the container to listen to requests on port 5000. This is necessary so that Docker can configure the network in the container appropriately.
EXPOSE 5000

# Run the server with gunicorn
# gunicorn will listen for requests on port 5000.
# gunicorn will handle 2 concurrent requests at a time
# gunicorn will look into the module called "application" and load from it the application instance called "application"
# gunicorn will use gevent workers
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:application", "--worker-class=gevent", "--workers=4"]