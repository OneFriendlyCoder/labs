# FROM ubuntu:latest

# # Installing common packages
# RUN apt-get update -y && apt-get install -y software-properties-common language-pack-en-base debconf-utils curl wget

# RUN ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
# RUN LC_ALL=en_US.UTF-8 add-apt-repository ppa:ondrej/php

# RUN apt-get update -y && apt-get install python3 python3-pip -y
# RUN apt-get update -y && apt-get install cron -y
# RUN apt-get install -y iputils-ping


# ENV DEBIAN_FRONTEND=noninteractive
# ENV DEBCONF_NONINTERACTIVE_SEEN=true


# RUN echo "tzdata tzdata/Areas select Europe" > /tmp/preseed.txt; \
#     echo "tzdata tzdata/Zones/Europe select Berlin" >> /tmp/preseed.txt; \
#     debconf-set-selections /tmp/preseed.txt && \
#     apt-get update && \
#     apt-get install -y tzdata

# RUN mkdir /home/labDirectory
# RUN mkdir /home/.evaluationScripts
# WORKDIR /home/labDirectory
# # EXPOSE 30001
# ENTRYPOINT ["/home/.evaluationScripts/server.sh"]


# #CMD [ "/bin/bash", "-c", "bash /home/.evaluationScripts/activityInitiator/initactivity.sh; while :; do sleep 10; done" ]



FROM ubuntu:jammy

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# Update and install required packages (including iproute2 and net-tools)
RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    net-tools \
    iproute2 \
    nano \
    jq \
    cron \
    zip \
    unzip \
    software-properties-common \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    lsb-release \
    xdg-utils \
    libgbm1 \
    gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pymongo and faker
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install pymongo faker bcrypt requests

# Install Node.js (version 16, which is above version 14)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get update && apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add MongoDB repository and install MongoDB
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --batch -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get install -y mongodb-org mongodb-mongosh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir -p /home/labDirectory /home/.evaluationScripts /var/log/mongodb /data/db && \
    chown -R mongodb:mongodb /data/db /var/log/mongodb

# Set default directory for the root user
RUN echo "cd /home/labDirectory" > /root/.bashrc

# (Optional) Copy directories to the container
# COPY labDirectory /home/labDirectory
# COPY .evaluationScripts /home/.evaluationScripts

# Set environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM="xterm"

# Switch to root for npm install
WORKDIR /home/labDirectory

# Expose MongoDB port
EXPOSE 27017

# Switch to the mongodb user
USER mongodb

# Start MongoDB and keep the container running
#CMD ["mongod", "--bind_ip_all", "--dbpath", "/data/db", "--logpath", "/var/log/mongodb/mongod.log", "--logappend"]

# ENTRYPOINT ["/bin/bash", "-c", "source /home/.evaluationScripts/entrypoint.sh"]

# Switch back to root if further operations are needed
USER root
ENTRYPOINT ["/home/.evaluationScripts/entrypoint.sh"]
