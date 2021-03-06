# pandemic-monitor
[![Build Status](https://travis-ci.org/pwegrzyn/pandemic-monitor.svg?branch=master)](https://travis-ci.org/pwegrzyn/pandemic-monitor)

Pandemic-Monitor is an app used to contain the spread of a virus during a pandemic.
A user installs the Android app on their phone, which regularly sends GeoLocation data to the
backend. When a patien is diagonsed with COVID-19, the user gets a notification on their phone
if they had potentially been in contact with this person in the last days.

## Getting Started:
The backend is implemented in the spirit of microservices. To get started just use docker-compose to setup the backend

```bash
docker-compose up --build
```

This will bring up 3 microservices, a job queue and a scalable group of worker processes.

To use the Android app - navigate to the MobileClient directory and follow the instructions
layed down in the README file. The Angular web client is located in the web-client directory.
