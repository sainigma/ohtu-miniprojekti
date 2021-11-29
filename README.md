# Ohtu-miniprojekti
![example workflow](https://github.com/sainigma/ohtu-miniprojekti/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/sainigma/ohtu-miniprojekti/branch/main/graph/badge.svg?token=MP92ZQ4DNH)](https://codecov.io/gh/sainigma/ohtu-miniprojekti)

## Backlogs
- [Product Backlog](https://docs.google.com/spreadsheets/d/1UTAB7X3for7kcB7_GlngaTnpXSxTQixwS3AyCQtQa9s/edit#gid=1)
- [Sprint 1 Backlog](https://docs.google.com/spreadsheets/d/1UTAB7X3for7kcB7_GlngaTnpXSxTQixwS3AyCQtQa9s/edit#gid=0)

## Installation

Install project dependencies with `poetry install`

## Development

### Commands

Go to the virtual environment with `poetry shell`

From poetry shell:

`python3 src/index.py` to run the application

`pytest src/tests` to run unit-tests

`pylint src` to run lint

### Definition of done

User story is tested with Robot Framework.

Main functionalities are tested.

CI-tests are passed.

Acceptance criteria met.
