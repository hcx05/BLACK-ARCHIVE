FROM black-archive-base:latest

# Selects which language content pack gets built into this image. The app
# code never branches on language at runtime - each language is a separate
# built image (see docker-compose.zh.yml), picked at build time here.
ARG LANG=en

RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    iptables \
    proxychains4 \
    mariadb-server \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# This node is dual-homed (DMZ + Internal) - LEDGER gateway + case API + DB
# socat installed for pivoting exercises

# Weak SSH config + authorized_keys writable (legacy gateway misconfig)
RUN mkdir -p /home/sysadmin/.ssh \
    && chmod 777 /home/sysadmin/.ssh

COPY app/api/ /opt/relay/api/
COPY sql/init.sql /opt/relay/sql/init.sql
COPY scripts/run-mariadb.sh /opt/relay/scripts/run-mariadb.sh

# Select the content pack for this build's LANG and drop the other one -
# server.js just requires ./content.js, it has no idea which language it is.
RUN cp /opt/relay/api/content_${LANG}.js /opt/relay/api/content.js \
    && rm -f /opt/relay/api/content_en.js /opt/relay/api/content_zh.js

# COPY preserves whatever mode these had in the build context (depends on
# the build host's umask) - lock down to sane defaults before re-marking
# the one script that actually needs +x.
RUN chown -R root:root /opt/relay \
    && find /opt/relay -type d -exec chmod 755 {} \; \
    && find /opt/relay -type f -exec chmod 644 {} \; \
    && chmod +x /opt/relay/scripts/run-mariadb.sh \
    && cd /opt/relay/api && npm install --production --no-audit --no-fund

RUN mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld

# ledger-cairn-sync service config (backs the account referenced in the
# API's system record and by the sync service itself, not a bare DB dump)
RUN mkdir -p /etc/ledger
COPY etc-ledger/ /etc/ledger/
COPY etc-ledger-zh/ /etc/ledger-zh/
RUN if [ "${LANG}" = "zh" ]; then cp /etc/ledger-zh/* /etc/ledger/; fi \
    && rm -rf /etc/ledger-zh \
    && chmod 644 /etc/ledger/sync.conf /etc/ledger/audit_note.txt

COPY config/supervisord.conf /etc/supervisor/conf.d/relay.conf
RUN chown root:root /etc/supervisor/conf.d/relay.conf && chmod 644 /etc/supervisor/conf.d/relay.conf

EXPOSE 22

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
