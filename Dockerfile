# Ubuntu 22.04 base image
FROM ubuntu:22.04

# Install Python
RUN apt-get -q update && DEBIAN_FRONTEND="noninteractive" apt-get -q install -y -o Dpkg::Options::="--force-confnew" --no-install-recommends build-essential python3-dev python3-pip && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy app
COPY app/ ./

# Run app
ENTRYPOINT ["/usr/bin/python3", "server.py"]
CMD ["-a", "0.0.0.0"]
EXPOSE 8001
