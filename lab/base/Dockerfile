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

# sysadmin is the one account genuinely shared across every host in this
# lab (webmail login that happens to double as the real OS account, relay
# SSH target, archive SMB user) - it belongs in the base image. Every
# other legacy account (devuser, deploy, backup, ...) used to be created
# here too, uniformly on every host regardless of whether that host's own
# story actually needed it - which is exactly backwards: devuser/deploy
# ended up with real, working logins everywhere even though the in-game
# documents describe them as rotated/decommissioned, and devuser's
# password worked as an unintended bypass on webmail. Accounts a specific
# host's story actually calls for (e.g. relay's `backup`) are created in
# that host's own Dockerfile instead - see lab/relay/Dockerfile.
RUN useradd -m -s /bin/bash sysadmin && echo "sysadmin:admin123" | chpasswd

RUN mkdir -p /var/run/sshd \
    && sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /var/log/supervisor

EXPOSE 22
