#!/bin/bash

NAME="sentiment-analy-app"
FLASKDIR=/home/sampathweb/projects/sentiment-analy-app/api
SOCKFILE=/home/sampathweb/sock
USER=sampathweb
GROUP=sampathweb
NUM_WORKERS=3

echo "Starting $NAME"

# activate the virtualenv
source /home/sampathweb/miniconda/bin/activate apps27

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Start your unicorn
exec gunicorn run:application -b 127.0.0.1:8002 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE