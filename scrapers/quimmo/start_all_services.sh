#!/bin/bash

# List of services to start
SERVICES=(
    "quimmo_worker1.service"
    "quimmo_worker2.service"
    "quimmo_worker3.service"
    "quimmo_worker4.service"
    "quimmo_worker5.service"
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
