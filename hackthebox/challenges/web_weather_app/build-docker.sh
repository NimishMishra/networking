#!/bin/bash
docker build --tag=weather_app .
docker run -p 1337:80 --rm --name=weather_app -it weather_app
