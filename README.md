# record-uploader.python

The applications demonstrates a simple ETL process, focusing on extracting and loading from S3 to DB
The python application takes a CSV file from S3, containing a list of data files to insert into Postgres.

## Prerequisites

- [Python](https://www.python.org/) 3.7+ `brew install python3`
- The modules in `requirements.txt` (see the *getting started* instructions below)
- [Docker](https://www.docker.com/products/docker-desktop)
- [JetBrains DataGrip](https://www.jetbrains.com/datagrip/features/mysql.html) IDE for working with databases

## Getting started

*Install on a local machine for development and testing purposes. See deployment for notes on how to convert the package into a distribution.*

- In your `.bash_profile` or `.zshrc`:
```
alias python=/usr/local/bin/python3

export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=$HOME/.virtualenvs

# Sourcing virtualenvwrapper
source ~/Library/Python/3.7/bin/virtualenvwrapper.sh
```
- Restart your terminal.

### Install into virtualenv

These steps should be familiar if you're familiar with python; if you're not, here's a brief guide to installing:

- Make sure you have virtualenvwrapper installed `pip3 install --user virtualenvwrapper`
- Create a virtualenv to hold the project, this will also create a virtual directory `python3 -m venv ~/.virtualenvs/record_uploader`
- Restart your terminal
- List virtual environments to verify they are showing up `lsvirtualenv`
- Activate using `workon record_uploader`
- Install the project into that virtualenv in development mode `make init-dev`
- Use `deactivate` to leave the virtual environment.

### Example execution

An example execution for running the application is shown below:

Run postgres docker container: 
> `docker-compose up`

Ensure you can connect (DataGrip IDE) to connection string
> Default port 5432 
> jdbc:postgresql://localhost:5432/postgres

Run [scripts](./sql-test/entrypoint) to setup schema and table


#### Running application

*Instructions on how to get a development environment running.*

- source into virtual env `source record_uploader`
- Run with default values: `make run`

Get info by running `record_uploader --help`

Alternatively, override default cli vars:
```
record_uploader -s source_bucket -k source_key -u my_user \         2 ↵
-d my_db -p 1234 -h localhost -b test-bucket
```

## Running the tests

Run unit tests and any linting checks.

- Run unit tests: `make test`
- Run sql_query tests: `cd ./sql-test/` and run `./run-tests.sh`

### Pylint & Flake8 Checks 

Pylint checks for bugs and code quality. It follows the style recommended by PEP 8, the Python style guide. Flake8 is used for checking your code base against coding style (PEP8). 
How to check your code for issues. 

1) Run `make analyze`
2) Fix all the issues reported by pylint
3) Re-run `make analyze`
4) If you see a score of 10/10 - submit your PR 

Guidelines when fixing pylint errors:

* Aim to fix the errors rather than disable the pylint checks - often you can easily refactor the code
  using your IDE
* When disabling a particular problem - make sure to disable only that error-via the symbolic name
  of the error as reported by pylint
* If there is a single line where to disable particular error you can add comment following the line
  that causes the problem. For example:
```python
def GetCustomer(dict_collection):   # pylint:   disable=invalid-name
```
* When there are multiple lines/block of code to disable an error you can surround the block with
  comment only pylint:disable/pylint:enable lines. For example:

```python
# pylint: disable=too-few-public-methods
class Counter(Words):
    """Count words for file"""
    filepath = StringField('Filepath', [InputRequired()])
# pylint: enable=too-few-public-methods
```

## Deployment

*Create a distribution from the project.*

- Build:
  - `make clean`
  - `make build`
- Deploy to AWS: **TODO**

## Source

[Docker_postgres](https://hub.docker.com/_/postgres)
