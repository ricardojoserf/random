#!/bin/bash
docker build -t flaskapp .
docker run -d -p $1:5000 flaskapp python app.py
