#!/bin/bash

cd frontend/stein_app

npm install -g @angular/cli
npm install
ng build

cd ../../backend

python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
