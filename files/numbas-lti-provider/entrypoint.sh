#!/bin/bash

while !</dev/tcp/postgres/5432;
    do echo "Waiting for psql"
    sleep 1
done

python3 numbas-setup.py 
