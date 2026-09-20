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

# COPY preserves whatever mode these files had in the build context, which
# depends on the umask of whoever ran the build - not something to rely on
# for security. Lock everything down to sane defaults regardless, then
# re-loosen only the specific paths that are supposed to be loose below.
RUN chown -R root:root /var/www/html/portal /opt/webmail /etc/nginx/sites-available/default \
    && find /var/www/html/portal /opt/webmail -type d -exec chmod 755 {} \; \
    && find /var/www/html/portal /opt/webmail -type f -exec chmod 644 {} \; \
    && chmod 644 /etc/nginx/sites-available/default

# Intentional misconfiguration (carried over from legacy ROSTER deployment):
# uploads/ has to stay writable by www-data for the intake form to work at
# all, and there's no extension allowlist/rename on top of that - that's
# the one deliberate foothold this host has. No local-root privesc lives
# here: root on this box wouldn't unlock anything past what the foothold
# already gives, so there isn't one to find.
RUN chmod -R 777 /var/www/html/portal/uploads

# Stale env vars from the last credential rotation on the webmail gateway
ENV SMTP_USER=duty.admin
ENV SMTP_PASS=MailP@ss2024
ENV SECRET_KEY=roster-webmail-secret-do-not-share

COPY config/supervisord.conf /etc/supervisor/conf.d/frontier.conf
RUN chown root:root /etc/supervisor/conf.d/frontier.conf && chmod 644 /etc/supervisor/conf.d/frontier.conf

EXPOSE 80 8025

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
