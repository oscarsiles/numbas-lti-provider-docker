#!/bin/bash

while !</dev/tcp/postgres/5432;
    do echo "Waiting for psql"
    sleep 1
done

if grep -Fq "{{HOST}}" numbasltiprovider/settings.py; then
	sed -i "s/{{HOST}}/${SERVERNAME}/" numbasltiprovider/settings.py
	sed -i "s/{{POSTGRES_PASSWORD}}/${POSTGRES_PASSWORD}/" numbasltiprovider/settings.py
	SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 64)
	sed -i "s/{{SECRET_KEY}}/${SECRET_KEY}/" numbasltiprovider/settings.py
	python3 numbas-setup.py 
fi

