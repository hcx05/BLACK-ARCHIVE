#!/bin/bash
set -e

if [ ! -d /var/lib/mysql/mysql ]; then
    mariadb-install-db --user=mysql --datadir=/var/lib/mysql > /dev/null 2>&1
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
