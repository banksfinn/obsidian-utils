from datetime import datetime, date
from constants import base_path
import os

years = [2022]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
path = base_path + "Bullet Journal/"

text = """---
tags:
- dailies
location: 
---

# Notes
- 

# To Do
- [ ] """
for year in years:
    for month in months:
        if month == 12:
            num_days = 31
        else:
            num_days = (date(year, month + 1, 1) - date(year, month, 1)).days
        month_text = date(1900, month, 1).strftime('%B')
        os.mkdir(path + f"{year}/{month} - {month_text}")
        for day in range(1, num_days + 1):
            cur_path = path + f"{year}/{month} - {month_text}/{month}-{day}-{year}.md"
            cur_day = open(cur_path, "w")
            cur_day.write(text)
            cur_day.close()
