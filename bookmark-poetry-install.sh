# !/bin/bash
#
tar -xvf ohtu-miniprojekti-0.1.0.tar.gz
cd ohtu-miniprojekti-0.1.0 #<--- Tähän viimeisin release

if ! command -v poetry &> /dev/null
then
	echo "Poetry installation required, do you wish to install it? (y/n)"

	read response
	if [[ ( $response == "y" ) ]]; then
		echo "Installing poetry...."
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
		poetry install
		poetry run python3 src
	else
		echo "Program requires poetry to be executed"
	fi
else
echo "Launching the program"
poetry install
poetry run python3 src
fi
