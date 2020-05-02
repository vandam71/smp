.ONESHELL:

GLOBAL_PYTHON = python3
PYTHON = ./env/bin/python3

install:
	$(PYTHON) -m pip install --upgrade -r requirements
	$(PYTHON) setup.py install

run:
	$(PYTHON) run.py

environment:
	$(GLOBAL_PYTHON) -m venv env

clean:
	$(PYTHON) setup.py clean

all:
	make clean install run
