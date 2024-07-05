#!/bin/bash

# List of services to start
SERVICES=(
    "fa_worker1.service"
    "fa_worker2.service"
    "fa_worker3.service"
    "fa_worker4.service"
    "fa_worker5.service"
)

# Start each service in the background
for SERVICE in "${SERVICES[@]}"
do
    echo "Starting $SERVICE..."
    sudo systemctl start $SERVICE &
    echo "$SERVICE started with PID $!"
done

# Wait for all background processes to complete
wait
echo "All aste services started"
