SHELL := /bin/bash
USER_FLAG := $(shell [[ -z $$VIRTUAL_ENV ]] && echo '--user')
.DEFAULT_GOAL := test
FORCE:

init:
	pip install $(USER_FLAG) -r requirements.txt

init-dev:	init
	pip install $(USER_FLAG) -r requirements-dev.txt

analyze:
# 	flake8 record_uploader
	pylint record_uploader

test: analyze
	nosetests  -s --with-coverage  --cover-package record_uploader --cover-inclusive --cover-html --cover-min-percentage 85  --cover-html-dir build/coverage

build: FORCE
	python setup.py bdist_wheel

install: build
	pip install $(USER_FLAG) --upgrade --force-reinstall dist/record_uploader-0.0.1-py3-none-any.whl

uninstall: FORCE
	pip uninstall $(USER_FLAG) -y record_uploader

clean:
	rm -rf ./build/
	rm -rf ./record_uploader.egg-info/
	rm -rf ./dist/
