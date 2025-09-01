# unix networking activity 1-6
FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-bs4 \
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
    language-pack-en-base \
    debconf-utils \
    iputils-ping \
    tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install pymongo faker bcrypt requests tinycss2 webcolors
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get update && apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --batch -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get install -y mongodb-org mongodb-mongosh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /home/labDirectory /home/.evaluationScripts /var/log/mongodb /data/db && \
    chown -R mongodb:mongodb /data/db /var/log/mongodb
RUN echo "cd /home/labDirectory" > /root/.bashrc
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM="xterm"
WORKDIR /home/labDirectory
EXPOSE 27017
USER mongodb
USER root
ENTRYPOINT ["/home/.evaluationScripts/entrypoint.sh"]