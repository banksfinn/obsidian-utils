from constants.journal_constants import (
    base_obsidian_vault_path,
    obsidian_dossier_path,
    birthday_calendar_note,
)
import glob
import regex

# Select the range of dates and months to be backfilled here
dossier_path = base_obsidian_vault_path + obsidian_dossier_path
birthday_note_path = base_obsidian_vault_path + birthday_calendar_note

# TODO: Support more birthday types
short_birthday_regex = r"birthday: (\d+\/\d+)"
long_birthday_regex = r"birthday: (\d+\/\d+)/\d+"

birthday_matchers = [short_birthday_regex, long_birthday_regex]

birthdays = {}

# Recursively look through dossier and grab the birthdays
for filename in glob.iglob(dossier_path + "**/*.md", recursive=True):
    name = filename.split("/")[-1][:-3]
    with open(filename, "r") as person:
        data = person.readlines()
        for line in data:
            for bm in birthday_matchers:
                birthday_date = regex.match(bm, line)
                if birthday_date:
                    actual_bday = birthday_date[1]
                    if actual_bday in birthdays:
                        birthdays[actual_bday].append(name)
                    else:
                        birthdays[actual_bday] = [name]
                    break

# Save the current data
existing_data = ""
with open(birthday_note_path, "r") as note:
    existing_data = note.read()

new_data = ""
month_index_skip = 1
day_index_skip = 2

# Loop through all of the rows
for day_index, row in enumerate(existing_data.split("\n")):
    new_row = ""
    values = []
    # Loop through each of the columns within a row
    for month_index, column in enumerate(row.split("|")):
        month = month_index - month_index_skip
        day = day_index - day_index_skip
        date_string = f"{month}/{day}"
        birthday_values = []
        # Check if there is a match
        if date_string in birthdays:
            # We have a birthday match!
            for name in birthdays[date_string]:
                if name not in column:
                    birthday_values.append("[[" + name + "]]")

        data_points = []
        if column.strip():
            data_points.append(column.strip())
        if birthday_values:
            data_points = data_points + birthday_values

        if not data_points:
            data_points.append("")

        values.append("<br>".join(data_points))

    new_data += "|".join(values) + "\n"

# Write to file!
new_data = new_data[:-1]
with open(birthday_note_path, "w") as f:
    f.write(new_data)
