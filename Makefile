#!/usr/bin/env make

VIRTUALENV := .venv
PIP = $(VIRTUALENV)/bin/pip

$(VIRTUALENV):
	virtualenv $(VIRTUALENV)

build: $(VIRTUALENV)
	$(PIP) install -r requirements.txt

.PHONY: build
.DEFAULT_GOAL := build
