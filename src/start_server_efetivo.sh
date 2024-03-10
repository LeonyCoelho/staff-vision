#!/bin/bash

# Ative o ambiente virtual
source /home/deploy/env-staff_vision/bin/activate

# Inicie o Gunicorn
gunicorn --config /home/deploy/staff_vision/conf/gunicorn_config.py --chdir /home/deploy/staff_vision/ staff_vision.wsgi:application

