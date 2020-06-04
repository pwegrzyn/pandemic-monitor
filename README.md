# pandemic-monitor
[![Build Status](https://travis-ci.org/pwegrzyn/pandemic-monitor.svg?branch=master)](https://travis-ci.org/pwegrzyn/pandemic-monitor)

Pandemic-Monitor is an app used to contain the spread of a virus during a pandemic.
A user installs the Android app on their phone, which regularly sends GeoLocation data to the
backend. When a patien is diagonsed with COVID-19, the user gets a notification on their phone
if they had potentially been in contact with this person in the last days.

## Getting Started:
Just use docker-compose to setup the backend

```bash
docker-compose build
docker-compose up
```

This will bring up 3 services, a job queue and a bunch of workers.

To use the Android app - navigate to the MobileClient directory and follow the instructions
layed down in the README file.