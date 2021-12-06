# Ohtu-miniprojekti
![example workflow](https://github.com/sainigma/ohtu-miniprojekti/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/sainigma/ohtu-miniprojekti/branch/main/graph/badge.svg?token=MP92ZQ4DNH)](https://codecov.io/gh/sainigma/ohtu-miniprojekti)

## Backlogs
- [Product Backlog](https://docs.google.com/spreadsheets/d/1UTAB7X3for7kcB7_GlngaTnpXSxTQixwS3AyCQtQa9s/edit#gid=1)
- [Sprint 1 Backlog](https://docs.google.com/spreadsheets/d/1UTAB7X3for7kcB7_GlngaTnpXSxTQixwS3AyCQtQa9s/edit#gid=0)
- [Sprint 2 Backlog](https://docs.google.com/spreadsheets/d/1UTAB7X3for7kcB7_GlngaTnpXSxTQixwS3AyCQtQa9s/edit#gid=8)

## Installation

Install project dependencies with `poetry install`

## Development

### Commands

Go to the virtual environment with `poetry shell`

From poetry shell:

`invoke start` to run the application

`invoke verify` to run unit-tests, Robot-tests and lint.

See [tasks.py](https://github.com/sainigma/ohtu-miniprojekti/blob/main/tasks.py) for all invoke tasks.

### Definition of done

User story is tested with Robot Framework imitating end-user behaviour.

Main functionalities are manually tested.

Our CI-pipeline passes.

\>70% Code coverage for unit-tests.

Acceptance criteria met.

### Robot tests

[All robot tests](https://github.com/sainigma/ohtu-miniprojekti/tree/main/src/tests/robot)
