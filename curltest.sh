#!/bin/bash

# Number of requests to send
REQUESTS=20

echo "Testing Load Balancing:"
for i in $(seq 1 $REQUESTS); do
    curl http://localhost
done | sort | uniq -c