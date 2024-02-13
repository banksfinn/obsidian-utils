#!/bin/bash
set -o pipefail

echo "Generating scripts virtual environment (python)"
python3 -m venv scripts/venv
source scripts/venv/bin/activate
pip install -r scripts/requirements.txt

cp constants/example_journal_constants.py constants/journal_constants.py
