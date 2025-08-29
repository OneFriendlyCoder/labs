FROM node:20

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip bash && \
    rm -rf /var/lib/apt/lists/*

ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM="xterm"

WORKDIR /home/labDirectory

CMD [ "bash", "-c", "while :; do sleep 10; done" ]
