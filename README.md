# PrayerBot [![Build Status](https://travis-ci.org/kubaodias/prayerbot.svg?branch=master)](https://travis-ci.org/kubaodias/prayerbot)

Environment variable ACCESS_TOKEN with your Facebook's page token has to be set.

### You can easily setup PrayerBot for development using Docker

Requirements:
* Docker engine (for OS X also docker-machine)
* docker-compose (`pip install docker-compose`)

To start app you just need to `docker-compose run web up`
To run test suite `docker-compose run web py.test`
