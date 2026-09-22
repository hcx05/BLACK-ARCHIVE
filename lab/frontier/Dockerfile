FROM black-archive-base:latest

# Selects which language content pack gets built into this image. The app
# code never branches on language at runtime - each language is a separate
# built image (see docker-compose.zh.yml), picked at build time here.
ARG LANG=en

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    php-fpm \
    php-mysql \
    php-xml \
    php-curl \
    && rm -rf /var/lib/apt/lists/*

# Normalize the fpm socket path across PHP versions so nginx.conf doesn't
# need to hardcode a version-specific socket name. Also disable clear_env -
# php-fpm strips the container's environment from workers by default, which
# would silently break getenv('WEBMAIL_PORT') (used by the portal's own
# webmail quicklink) and any future env-based config.
RUN PHP_INI_DIR=$(ls -d /etc/php/*/fpm | head -n1) \
    && sed -i 's|^listen = .*|listen = /run/php/php-fpm.sock|' "$PHP_INI_DIR/pool.d/www.conf" \
    && sed -i 's|^;clear_env = no|clear_env = no|' "$PHP_INI_DIR/pool.d/www.conf"

# ROSTER terminal (public portal) + webmail
COPY app/portal/ /var/www/html/portal/
COPY app/webmail/ /opt/webmail/
COPY config/nginx.conf /etc/nginx/sites-available/default

# Select the content pack for this build's LANG and drop the other one -
# index.php just requires content.php, it has no idea which language it is.
RUN cp /var/www/html/portal/content_${LANG}.php /var/www/html/portal/content.php \
    && rm -f /var/www/html/portal/content_en.php /var/www/html/portal/content_zh.php \
    && cp /opt/webmail/content_${LANG}.py /opt/webmail/content.py \
    && rm -f /opt/webmail/content_en.py /opt/webmail/content_zh.py \
    && if [ -d "/var/www/html/portal/notes-${LANG}" ]; then \
         rm -rf /var/www/html/portal/notes && mv /var/www/html/portal/notes-${LANG} /var/www/html/portal/notes; \
       fi \
    && rm -rf /var/www/html/portal/notes-en /var/www/html/portal/notes-zh

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

# Host-published webmail port, so the portal's own "Webmail" quicklink
# points somewhere that actually resolves - the container only knows its
# own internal port (8025), not which host port a given compose file
# publishes it as. Override per-deployment in docker-compose*.yml.
ENV WEBMAIL_PORT=8025

COPY config/supervisord.conf /etc/supervisor/conf.d/frontier.conf
RUN chown root:root /etc/supervisor/conf.d/frontier.conf && chmod 644 /etc/supervisor/conf.d/frontier.conf

EXPOSE 80 8025

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
