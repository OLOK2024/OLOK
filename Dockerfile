FROM node:20.9.0

# Set the working directory
WORKDIR /usr/src/app

# Add the source code to app
COPY ./FrontEnd /usr/src/app/

# Install angular CLI
RUN npm install -g @angular/cli

# Install all the dependencies
RUN npm install

# Install boostrap
RUN npm install bootstrap

# Expose port 4200
EXPOSE 4200

# Start the application
CMD ["ng", "serve", "--host", "0.0.0.0"]