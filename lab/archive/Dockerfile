FROM black-archive-base:latest

# Selects which language content pack gets built into this image. The app
# code never branches on language at runtime - each language is a separate
# built image (see docker-compose.zh.yml), picked at build time here.
ARG LANG=en

RUN apt-get update && apt-get install -y --no-install-recommends \
    samba \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY smb/smb.conf /etc/samba/smb.conf
RUN chown root:root /etc/samba/smb.conf && chmod 644 /etc/samba/smb.conf

# Restricted disposition-hold shares
RUN mkdir -p /srv/share/public /srv/share/confidential /srv/share/backups \
    && chmod 777 /srv/share/public \
    && chmod 755 /srv/share/confidential \
    && chmod 777 /srv/share/backups
COPY shares/public/ /srv/share/public/
COPY shares/confidential/ /srv/share/confidential/
COPY shares/backups/ /srv/share/backups/
COPY shares-zh/public/ /srv/share-zh/public/
COPY shares-zh/confidential/ /srv/share-zh/confidential/
COPY shares-zh/backups/ /srv/share-zh/backups/
RUN if [ "${LANG}" = "zh" ]; then \
      cp /srv/share-zh/public/* /srv/share/public/ 2>/dev/null || true; \
      cp /srv/share-zh/confidential/* /srv/share/confidential/ 2>/dev/null || true; \
      cp /srv/share-zh/backups/* /srv/share/backups/ 2>/dev/null || true; \
    fi \
    && rm -rf /srv/share-zh \
    && chmod 644 /srv/share/confidential/* /srv/share/backups/*

# Set Samba password for the sysadmin (base) account. Same password as
# everywhere else - whoever provisioned this never rotates per-service.
RUN (echo "admin123"; echo "admin123") | smbpasswd -a -s sysadmin

# This node was hardened past the base image's password-auth default:
# shell access requires the backup/restore key, not the reused OS password.
# Samba above and the reused password elsewhere are untouched - only this
# node's SSH stopped accepting it.
RUN sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config \
    && mkdir -p /home/sysadmin/.ssh \
    && chmod 700 /home/sysadmin/.ssh
COPY ssh/authorized_keys /home/sysadmin/.ssh/authorized_keys
RUN chmod 600 /home/sysadmin/.ssh/authorized_keys \
    && chown -R sysadmin:sysadmin /home/sysadmin/.ssh

COPY app/admin/admin_panel.py /opt/admin/app.py
COPY app/admin/content_en.py app/admin/content_zh.py /opt/admin/
COPY app/admin/assets/ /opt/admin/assets/
RUN cp /opt/admin/content_${LANG}.py /opt/admin/content.py \
    && rm -f /opt/admin/content_en.py /opt/admin/content_zh.py
# app.py/content.py/assets stay root-owned and read-only; the directory
# itself is group-writable (sticky bit set) only so the app - running as
# www-data, see supervisord.conf - can create its own admin.db at first
# startup without being able to delete or replace the protected files above.
RUN chown -R root:root /opt/admin \
    && find /opt/admin -type d -exec chmod 755 {} \; \
    && find /opt/admin -type f -exec chmod 644 {} \; \
    && chown root:www-data /opt/admin \
    && chmod 1775 /opt/admin

# Final root-gated disposition summary
COPY root/cairn_disposition_review.txt /root/cairn_disposition_review.txt
COPY root-zh/cairn_disposition_review.txt /root/cairn_disposition_review_zh.txt
RUN if [ "${LANG}" = "zh" ]; then mv /root/cairn_disposition_review_zh.txt /root/cairn_disposition_review.txt; \
    else rm -f /root/cairn_disposition_review_zh.txt; fi \
    && chmod 600 /root/cairn_disposition_review.txt

# Root cron healthcheck job (privilege escalation via PATH resolution, not a
# writable script). /opt/staging is a leftover deployment directory from the
# last CAIRN rollout - never cleaned up, still group-writable to the
# release group, and still ahead of the system dirs in root's crontab PATH.
# logtool itself was never actually shipped anywhere on the real PATH, so
# this job has been silently failing since the rollout.
# NOTE: this group must NOT be named "deploy" - the base image already ships
# a "deploy" user whose primary group of the same name would silently
# inherit this access too, handing root to that dead account for free.
RUN groupadd release \
    && usermod -aG release sysadmin \
    && mkdir -p /opt/staging \
    && chown root:release /opt/staging \
    && chmod 775 /opt/staging \
    && printf '#!/bin/bash\nlogtool "Health check: $(date)" >> /var/log/health.log\n' > /opt/healthcheck.sh \
    && chown root:release /opt/healthcheck.sh \
    && chmod 750 /opt/healthcheck.sh \
    && echo "PATH=/opt/staging:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> /etc/crontab \
    && echo "* * * * * root /opt/healthcheck.sh" >> /etc/crontab

COPY config/supervisord.conf /etc/supervisor/conf.d/archive.conf
RUN chown root:root /etc/supervisor/conf.d/archive.conf && chmod 644 /etc/supervisor/conf.d/archive.conf

EXPOSE 139 445 8080

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
