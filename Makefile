.ONESHELL:

GLOBAL_PYTHON = python3
PYTHON = ./env/bin/python3

install:
	$(PYTHON) -m pip install --upgrade -r requirements

run:
	$(PYTHON) run.py

environment:
	$(GLOBAL_PYTHON) -m venv env

clean:
	$(PYTHON) -m pip freeze | xargs $(PYTHON) -m pip uninstall -y
	rm -f *.pyc

all:
	make clean environment install run
