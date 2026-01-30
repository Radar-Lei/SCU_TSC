FROM unsloth/unsloth:dgxspark-latest

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    SUMO_HOME=/usr/share/sumo \
    TZ=Asia/Shanghai

RUN apt-get update -o Acquire::Retries=5 && \
    apt-get install -o Acquire::Retries=5 -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        tzdata \
        software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:sumo/stable -y && \
    apt-get update -o Acquire::Retries=5 && \
    apt-get install -o Acquire::Retries=5 -y --no-install-recommends \
        sumo sumo-tools sumo-doc \
        mesa-utils libgl1-mesa-dri libglx-mesa0 libglu1-mesa \
        fluxbox x11-utils x11vnc xvfb && \
    rm -rf /var/lib/apt/lists/*

RUN pip install traci modelscope --break-system-packages

ENV PATH="${SUMO_HOME}/bin:${PATH}"
