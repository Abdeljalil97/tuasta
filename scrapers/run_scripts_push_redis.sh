#!/bin/bash

# Run Script astegiudiziarie
cd /home/web_scraper/scrapers/astegiudiziarie
/usr/bin/python3 red.py

# Run Script quimmo
cd /home/web_scraper/scrapers/quimmo
/usr/bin/python3 push_to_redis.py

# Run Script fallcoaste
cd /home/web_scraper/scrapers/fallcoaste
/usr/bin/python3 push_to_redis.py

# Run Script astalegale
cd /home/web_scraper/scrapers/astalegale
/usr/bin/python3 add_urls_to_redis.py



# Sleep for 24 hours
sleep 86400
