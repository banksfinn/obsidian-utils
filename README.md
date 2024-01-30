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

The list of python helper scripts that I use and maintain in obsidian.

#### Backfill Journal Days

Bulk generate old Bullet Journal notes. The text being used to populate these can be edited (and have significantly more logic put into it).

#### Populate Weeks

Generate week notes for a given year, such as Week 1 - 2024. I personally use these notes for a weekly review and retrospection.

### Dataview

Some functions that I use throughout my code that are useful!

#### Retrospective Analysis

This is used in my Weekly, Monthly, and Yearly templates to provide a retrospective on the tags used.

### Templates

These are all of the templates that I currently use in obsidian.

They are personalized to my use case, but there are parts of the code that might be useful to other people.

#### Today

I use the "Simple Templates/Today.md" template in combination with the hotkey system (and Templater). This allows me to use a hotkey to generate in today's date (I have it set to Command + G). This is super useful for work related purposes, specifically generating daily meeting notes.