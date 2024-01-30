from constants.journal_constants import (
    base_obsidian_vault_path,
    weekly_template_path,
    obsidian_journal_path,
)
from dateutil import parser
import datetime
import shutil

# Input the year to generate
year = int(input("What year: "))

# Determine the starting date for the year, aka find where week 1 starts
starting_date = parser.parse(str(year)).replace(
    month=1, day=1, hour=0, second=0, minute=0
)
while starting_date.weekday() != 0:
    starting_date = starting_date + datetime.timedelta(days=1)

# Feel free to change up the path here if you use a different system
weekly_folder_path = (
    base_obsidian_vault_path + obsidian_journal_path + f"/{year}/Weekly/"
)


# Iterate through each date
position = starting_date
ending_date = starting_date.replace(year=year + 1)
week_count = 1
while position < ending_date:
    # Generate the file path
    file_path = weekly_folder_path + f"Week {week_count} - {year}.md"
    # The starting date of that week
    starting_date = position
    # The ending date of that week
    ending_date = position + datetime.timedelta(days=6)

    # Increment the position
    position = position + datetime.timedelta(days=7)
    week_count += 1

    # Copy the Weekly Template to be the base of the new file
    shutil.copyfile(base_obsidian_vault_path + weekly_template_path, file_path)

    with open(file_path, "r") as f:
        contents = f.readlines()

    # Insert in the relevant dates to the file
    contents.insert(
        6,
        f"## [[{starting_date.strftime('%-m-%-d-%Y')}]] - [[{ending_date.strftime('%-m-%-d-%Y')}]]\n",
    )

    with open(file_path, "w") as f:
        contents = "".join(contents)
        f.write(contents)
