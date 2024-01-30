from datetime import date
from constants.journal_constants import base_obsidian_vault_path, obsidian_journal_path
import os


# Select the range of dates and months to be backfilled here
years = [2023]
months = [1, 2, 3]

journal_path = base_obsidian_vault_path + obsidian_journal_path

# Fill in the text you want to be backfilled here
text = """---
tags:
- dailies
location: 
---

# Notes
- 

"""

for year in years:
    for month in months:
        if month == 12:
            num_days = 31
        else:
            num_days = (date(year, month + 1, 1) - date(year, month, 1)).days
        month_text = date(1900, month, 1).strftime("%B")
        os.mkdir(journal_path + f"{year}/{month} - {month_text}")
        for day in range(1, num_days + 1):
            cur_path = (
                journal_path + f"{year}/{month} - {month_text}/{month}-{day}-{year}.md"
            )
            cur_day = open(cur_path, "w")
            cur_day.write(text)
            cur_day.close()
