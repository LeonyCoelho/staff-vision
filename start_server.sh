#!/bin/bash

# Ative o ambiente virtual
source /home/deploy/env-controle-efetivos/bin/activate

# Inicie o Gunicorn
gunicorn --config /home/deploy/controle_efetivos/conf/gunicorn_config.py --chdir /home/deploy/controle_efetivos/ controle_efetivos.wsgi:application --workers=2 --threads=2 --worker-class=gthread

