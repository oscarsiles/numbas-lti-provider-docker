#!/bin/bash

while !</dev/tcp/db/5432;
    do echo "Waiting for psql"
    sleep 1
done

if [ ! -f /srv/numbas-lti-provider/numbasltiprovider/settings.py ]; then
    cd /srv/numbas-lti-provider
    python3 first_setup.py
fi

/usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
