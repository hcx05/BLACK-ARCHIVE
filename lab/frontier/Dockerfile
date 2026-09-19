FROM black-archive-base:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    php-fpm \
    php-mysql \
    php-xml \
    php-curl \
    && rm -rf /var/lib/apt/lists/*

# Normalize the fpm socket path across PHP versions so nginx.conf doesn't
# need to hardcode a version-specific socket name.
RUN PHP_INI_DIR=$(ls -d /etc/php/*/fpm | head -n1) \
    && sed -i 's|^listen = .*|listen = /run/php/php-fpm.sock|' "$PHP_INI_DIR/pool.d/www.conf"

# ROSTER terminal (public portal) + webmail
COPY app/portal/ /var/www/html/portal/
COPY app/webmail/ /opt/webmail/
COPY config/nginx.conf /etc/nginx/sites-available/default

# Intentional misconfigurations (carried over from legacy ROSTER deployment)
RUN chmod -R 777 /var/www/html/portal/uploads \
    && echo "sysadmin ALL=(ALL) NOPASSWD: /usr/bin/find" >> /etc/sudoers

# Writable "backup" cron job run as root (privesc vector)
RUN printf '#!/bin/bash\ntar czf /backups/roster-backup.tar.gz /var/www/html/portal/\n' > /opt/backup.sh \
    && chmod 777 /opt/backup.sh \
    && mkdir -p /backups \
    && echo "*/5 * * * * root /opt/backup.sh" >> /etc/crontab

# Stale env vars from the last credential rotation on the webmail gateway
ENV SMTP_USER=duty.admin
ENV SMTP_PASS=MailP@ss2024
ENV SECRET_KEY=roster-webmail-secret-do-not-share

COPY config/supervisord.conf /etc/supervisor/conf.d/frontier.conf

EXPOSE 80 8025

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
