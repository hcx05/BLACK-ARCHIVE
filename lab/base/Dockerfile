FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    net-tools \
    iputils-ping \
    iproute2 \
    dnsutils \
    cron \
    curl \
    wget \
    vim-tiny \
    ncat \
    sudo \
    openssh-server \
    supervisor \
    python3 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Legacy UNSC logistics-network accounts. Original provisioning script is long gone;
# these were never rotated after the migration off the old personnel system.
# Ubuntu ships a system "backup" account with no shell/home - remove it first so
# our login-capable version can take the name.
RUN userdel -r backup 2>/dev/null; \
    useradd -m -s /bin/bash sysadmin && echo "sysadmin:admin123" | chpasswd \
    && useradd -m -s /bin/bash devuser && echo "devuser:devuser2024" | chpasswd \
    && useradd -m -s /bin/bash backup  && echo "backup:backup"      | chpasswd \
    && useradd -m -s /bin/bash deploy  && echo "deploy:deploy!"     | chpasswd

RUN mkdir -p /var/run/sshd \
    && sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /var/log/supervisor

EXPOSE 22
