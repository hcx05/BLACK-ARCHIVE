FROM black-archive-base:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    samba \
    redis-server \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY smb/smb.conf /etc/samba/smb.conf

# Redis with no authentication (intentional misconfiguration)
RUN sed -i 's/^bind .*/bind 0.0.0.0/' /etc/redis/redis.conf \
    && sed -i 's/^protected-mode yes/protected-mode no/' /etc/redis/redis.conf \
    && sed -i 's/^daemonize yes/daemonize no/' /etc/redis/redis.conf

# Restricted disposition-hold shares
RUN mkdir -p /srv/share/public /srv/share/confidential /srv/share/backups \
    && chmod 777 /srv/share/public \
    && chmod 755 /srv/share/confidential \
    && chmod 755 /srv/share/backups
COPY shares/public/ /srv/share/public/
COPY shares/confidential/ /srv/share/confidential/
COPY shares/backups/ /srv/share/backups/
RUN chmod 644 /srv/share/confidential/* /srv/share/backups/*

# Set Samba password for the sysadmin (base) account. Same password as
# everywhere else - whoever provisioned this never rotates per-service.
RUN (echo "admin123"; echo "admin123") | smbpasswd -a -s sysadmin

COPY app/admin/admin_panel.py /opt/admin/app.py
COPY app/admin/assets/ /opt/admin/assets/

# Final root-gated disposition summary
COPY root/cairn_disposition_review.txt /root/cairn_disposition_review.txt
RUN chmod 600 /root/cairn_disposition_review.txt

# Root cron healthcheck job (privilege escalation via PATH resolution, not a
# writable script). /opt/staging is a leftover deployment directory from the
# last CAIRN rollout - never cleaned up, still group-writable to the
# deploy group, and still ahead of the system dirs in root's crontab PATH.
# logtool itself was never actually shipped anywhere on the real PATH, so
# this job has been silently failing since the rollout.
RUN groupadd -f deploy \
    && usermod -aG deploy sysadmin \
    && mkdir -p /opt/staging \
    && chown root:deploy /opt/staging \
    && chmod 775 /opt/staging \
    && printf '#!/bin/bash\nlogtool "Health check: $(date)" >> /var/log/health.log\n' > /opt/healthcheck.sh \
    && chown root:deploy /opt/healthcheck.sh \
    && chmod 750 /opt/healthcheck.sh \
    && echo "PATH=/opt/staging:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> /etc/crontab \
    && echo "* * * * * root /opt/healthcheck.sh" >> /etc/crontab

COPY config/supervisord.conf /etc/supervisor/conf.d/archive.conf

EXPOSE 139 445 6379 8080

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
