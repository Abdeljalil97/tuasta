#!/bin/bash

# List of services to start
SERVICES=(
    "astalegale_worker1.service"
    "astalegale_worker2.service"
    "astalegale_worker3.service"
    "astalegale_worker4.service"
    "astalegale_worker5.service"
    
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
