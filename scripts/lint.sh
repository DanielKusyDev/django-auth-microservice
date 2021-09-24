#!/usr/bin/bash

poetry run isort . --check
poetry run black . --check