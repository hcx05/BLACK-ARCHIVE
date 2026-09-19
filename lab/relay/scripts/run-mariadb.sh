#!/bin/bash
set -e

# NOTE: the mariadb-server apt package's postinst already runs its own
# install/bootstrap at IMAGE BUILD TIME, so /var/lib/mysql/mysql always
# exists by the time this script runs - that is NOT a valid "first boot"
# signal. Check for our own database instead.
if [ ! -d /var/lib/mysql/ledger ]; then
    /usr/sbin/mariadbd --user=mysql --skip-networking --socket=/run/mysqld/mysqld.sock &
    tmp_pid=$!
    until mariadb --socket=/run/mysqld/mysqld.sock -u root -e "SELECT 1" > /dev/null 2>&1; do
        sleep 1
    done
    mariadb --socket=/run/mysqld/mysqld.sock -u root < /opt/relay/sql/init.sql
    mysqladmin --socket=/run/mysqld/mysqld.sock -u root shutdown
    wait "$tmp_pid" || true
fi

exec /usr/sbin/mariadbd --user=mysql --bind-address=0.0.0.0
