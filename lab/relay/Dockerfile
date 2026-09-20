FROM black-archive-base:latest

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

# SUID binary for privilege escalation (leftover diagnostic tool)
RUN cp /usr/bin/python3 /usr/local/bin/python3-suid \
    && chmod u+s /usr/local/bin/python3-suid

COPY app/api/ /opt/relay/api/
COPY sql/init.sql /opt/relay/sql/init.sql
COPY scripts/run-mariadb.sh /opt/relay/scripts/run-mariadb.sh
RUN chmod +x /opt/relay/scripts/run-mariadb.sh \
    && cd /opt/relay/api && npm install --production --no-audit --no-fund

RUN mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld

# ledger-cairn-sync service config (backs the account referenced in the
# API's system record and by the sync service itself, not a bare DB dump)
RUN mkdir -p /etc/ledger
COPY etc-ledger/sync.conf /etc/ledger/sync.conf
COPY etc-ledger/audit_note.txt /etc/ledger/audit_note.txt
RUN chmod 644 /etc/ledger/sync.conf /etc/ledger/audit_note.txt

COPY config/supervisord.conf /etc/supervisor/conf.d/relay.conf

EXPOSE 22

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
