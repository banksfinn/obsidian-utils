from constants.journal_constants import (
    base_obsidian_vault_path,
    obsidian_journal_path,
)
import datetime
from dateutil import parser

raw_year = input("What year do you want to generate: ")
year = int(raw_year)

# Select the range of dates and months to be backfilled here
schedule_path = (
    base_obsidian_vault_path
    + obsidian_journal_path
    + str(year)
    + "/"
    + str(year)
    + " Schedule 2.md"
)


starting_date = parser.parse(str(year)).replace(
    month=1, day=1, hour=0, second=0, minute=0
)

weekday_lookup = {
    "Sunday": "----- S -----",
    "Monday": "----- M -----",
    "Tuesday": "----- T -----",
    "Wednesday": "----- W -----",
    "Thursday": "----- T -----",
    "Friday": "----- F -----",
    "Saturday": "----- S -----",
}

contents = ""

# Iterate through each date
position = starting_date
ending_date = starting_date.replace(year=year + 1)

while position.year == year:
    month = position.strftime("%B")

    contents += "# " + month + "\n"
    contents += "| <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sun&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mon&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tue&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wed&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Thu&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fri&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> | <nobr>**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sat&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**</nobr> |\n"

    # contents += "| <nobr>***---- Sun ----***</nobr> | <nobr>***---- Mon ----***</nobr> | <nobr>***---- Tue ----***</nobr> | <nobr>***---- Wed ----***</nobr> | <nobr>***---- Thu ----***</nobr> | <nobr>***---- Fri ----***</nobr> | <nobr>***---- Sat ----***</nobr> |\n"
    contents += "| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |\n"

    # Get sunday as position 0
    for i in range(((position.weekday() + 1) % 7)):
        contents += "| "

    while position.strftime("%B") == month:
        contents += "| ***" + str(position.day) + "*** <br><br> "
        if position.weekday() == 5:
            contents += "|\n"

        position = position + datetime.timedelta(days=1)

    for i in range(7 - (position.weekday() + 1 % 7)):
        contents += "| "

    contents += "|\n"


with open(schedule_path, "w") as f:
    contents = "".join(contents)
    f.write(contents)
