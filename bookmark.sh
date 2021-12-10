#!/bin/bash

cd ohtu-miniprojekti-0.1.0 #<--- Tähän viimeisin release

if ! [$type "poetry" ]; then
	echo "In order to run the program poetry is needed. Do you wish to install it? (y/n)"
	
	read response
	if [[ ( $response == "y" ) ]]; then
		echo "Installing poetry...."
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
		poetry install
		poetry run python3 src/
	else
		echo "Program requires poetry to be executed"
	fi
else
	echo "Launching the program"
	poetry install
	poetry run python3 src/
fi
