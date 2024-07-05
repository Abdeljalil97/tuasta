#!/bin/bash

# List of services to start
SERVICES=(
    "aste_worker1.service"
    "aste_worker2.service"
    "aste_worker3.service"
    "aste_worker4.service"
    "aste_worker5.service"
    "aste_worker6.service"
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
