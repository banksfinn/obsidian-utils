from datetime import date
from constants.journal_constants import (
    base_obsidian_vault_path,
    obsidian_dossier_path,
    birthday_calendar_note,
)
import os
import glob
import regex

# Select the range of dates and months to be backfilled here
dossier_path = base_obsidian_vault_path + obsidian_dossier_path
birthday_note_path = base_obsidian_vault_path + birthday_calendar_note

# TODO: Support more birthday types
birthday_regex = r"birthday: (\d+\/\d+)"

birthdays = {}

# Recursively look through dossier and grab the birthdays
for filename in glob.iglob(dossier_path + "**/*.md", recursive=True):
    name = filename.split("/")[-1][:-3]
    with open(filename, "r") as person:
        data = person.readlines()
        for line in data:
            birthday_date = regex.match(birthday_regex, line)
            if birthday_date:
                birthdays[name] = birthday_date[1]

print(birthdays)

# TODO: Add this to the birthday table
