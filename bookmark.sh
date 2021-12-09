#!/bin/bash

cd ohtu-miniprojekti-0.1.0

if ! [$type "poetry" ]; then
	echo "In order to run the program poetry is needed. Do you wish to install it? (y/n)"
	
	read response
	if [[ ( $response == "y" ) ]]; then
		echo "Installing poetry...."
		pip install --user poetry
		poetry install
		poetry run python3 src/
	fi
else
	echo "Launching the program"
	poetry install
	poetry run python3 src/
fi
