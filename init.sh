#!/bin/sh

echo "STARTING SERVICES"
supervisord -c /fampay_assignment/background.conf &&
cd fampay_api && gunicorn fampay_api.wsgi:application --bind 0.0.0.0:8000
echo "SERVICES STARTED"
