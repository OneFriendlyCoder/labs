# Stage 1: Use a Node.js image for the first stage
FROM ubuntu:22.04 as ubuntu-stage

# Installing common packages
RUN yes | unminimize
RUN apt-get update -y && apt-get install -y software-properties-common language-pack-en-base debconf-utils curl
RUN apt-get update -y && apt-get install net-tools wget nano vim less -y
RUN apt-get update -y && apt-get install iproute2 python3.11 python3-pip -y

# Install anything you want here:
RUN apt-get install -y man-db
RUN apt-get install -y zip

# Install selenium & chrome
RUN pip install selenium

# Install chromium
RUN add-apt-repository ppa:xtradeb/apps -y
RUN apt update
RUN apt install -y chromium --no-install-recommends

# Determine architecture and download the correct chromedriver
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
        wget -O /tmp/chromedriver.zip https://github.com/electron/electron/releases/download/v34.0.2/chromedriver-v34.0.2-linux-arm64.zip; \
    else \
        wget -O /tmp/chromedriver.zip https://github.com/electron/electron/releases/download/v34.0.2/chromedriver-v34.0.2-linux-x64.zip; \
    fi
RUN unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -f /tmp/chromedriver.zip


# Setup Environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color

# Setup Directory Structure
RUN mkdir /home/labDirectory
RUN mkdir /home/.evaluationScripts

# Global Settings
RUN echo "cd /home/labDirectory" > /root/.bashrc
RUN echo "alias ls='ls --color=always'" >> /root/.bashrc
RUN echo "rm -f \`find /home -type f -name \"._*\"\`" >> /root/.bashrc
RUN apt install -y gdb --no-install-recommends
RUN pip install beautifulsoup4 GitPython
RUN apt-get update && apt-get install -y git

CMD [ "/bin/bash", "-c", "while :; do sleep 10; done" ]

