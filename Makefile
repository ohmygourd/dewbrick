#!/usr/bin/env make

WHICH_PYTHON := $(shell which python3)
VIRTUALENV := env
PYTHON := $(VIRTUALENV)/bin/python
PIP := $(VIRTUALENV)/bin/pip
APP := $(VIRTUALENV)/bin/dewbrick-app

$(VIRTUALENV):
	virtualenv -p $(WHICH_PYTHON) $(VIRTUALENV)

build: $(VIRTUALENV)
	$(PYTHON) setup.py develop

$(APP):
	$(MAKE) build

run: $(APP)
	$(APP)

clean:
	-rm -r env
	-rm -r *.egg*

.PHONY: build clean
.DEFAULT_GOAL := build
