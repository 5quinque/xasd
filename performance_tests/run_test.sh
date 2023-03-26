#!/bin/bash

tests=("soak" "peak" "quick")

if [[ -z "$1" ]]; then
    TEST="quick"
elif [[ ! "${tests[*]}" =~ "${1}" ]]; then
    echo "Not Valid test, either 'soak', 'peak', or 'quick'"
else
    TEST=$1
fi

# docker-compose -f provisioning/docker-compose.yml up -d


# Start the mite components
mite runner --controller-socket=tcp://127.0.0.1:14301 --message-socket=tcp://127.0.0.1:14302 &
mite runner --controller-socket=tcp://127.0.0.1:14301 --message-socket=tcp://127.0.0.1:14302 &
mite duplicator --message-socket=tcp://0.0.0.0:14302 tcp://0.0.0.0:14303 &
mite stats --stats-in-socket=tcp://127.0.0.1:14303 --stats-out-socket=tcp://0.0.0.0:14305 --stats-include-processors=mite,mite_http &
mite prometheus_exporter --stats-out-socket=tcp://127.0.0.1:14305 --web-address=0.0.0.0:9301 &

mite controller --controller-socket=tcp://0.0.0.0:14301 --message-socket=tcp://127.0.0.1:14302 scenarios:${TEST}_scenario &

echo "Open grafana in your browser http://localhost:3000/d/2_KG1Va7z/mite-docker?orgId=1&refresh=10s"


# sleep forever
while true; do sleep 1000; done

