#!/bin/bash

python -m virtualenv venv
. venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
echo "Vaccinchat Reviewer installed!"
