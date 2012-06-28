#!/bin/bash
export PYTHONPATH=..
coverage run run.py && coverage html && open htmlcov/index.html
