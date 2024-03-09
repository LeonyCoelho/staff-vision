#!/bin/bash

# Ative o ambiente virtual
source /home/deploy/env-controle-de-efetivo/bin/activate

# Inicie o Gunicorn
gunicorn --config /home/deploy/controle-de-efetivo/conf/gunicorn_config.py --chdir /home/deploy/controle-de-efetivo/ controle_efetivos.wsgi:application

