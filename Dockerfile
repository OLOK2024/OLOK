FROM node:20.11.1

# Set the working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY ./FrontEnd /usr/local/app/

# Install all the dependencies
RUN npm install

# Install angular CLI
RUN npm install -g @angular/cli

# Install boostrap
RUN npm install bootstrap

# Install compatibility 
RUN if [ "$(uname -m)" = "aarch64" ]; then npm i @rollup/rollup-linux-arm64-gnu; fi

# Expose port 4200
EXPOSE 4200

# Start the application
CMD ["ng", "serve", "--host", "0.0.0.0"]