# Obsidian Utils

## Summary

List of utility files, scripts, and other helpful bits that I use in my obsidian!

This repo is laid out on a folder system, so I'll be using that to tabulate the functionality.

## Installation

For the scripts, python is required. The virtual environment for this can be run using the setup script:
```
./setup.sh
```

After this has been done, the user can activate the virtual environment and run the relevant scripts.
```
source scripts/venv/bin/activate
python scripts/populate_weeks.py
```

All of the scripts have been designed to be run from the base of this repo.

## Contents

### Scripts

#### Backfill Journal Days

Bulk generate old Bullet Journal notes. The text being used to populate these can be edited (and have significantly more logic put into it).

#### Populate Weeks

Generate week notes for a given year, such as Week 1 - 2024. I personally use these notes for a weekly review and retrospection.

