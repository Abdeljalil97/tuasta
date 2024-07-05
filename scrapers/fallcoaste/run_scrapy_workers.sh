#!/bin/bash
cd /home/web_scraper/scrapers/fallcoaste

# Activate the virtual environment
source /home/web_scraper/scrapers/venv/bin/activate

# Define the number of processes
num_processes=6

# Start the processes
for i in $(seq 1 $num_processes); do
    python3 worker1.py &
done

# Wait for all processes to complete
wait
