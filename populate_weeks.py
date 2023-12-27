from constants import base_path
from dateutil import parser
import datetime
import shutil


year = 2023
template_path = "Templates/Weekly Template.md"
local_path = f"Bullet Journal/{year}/Weekly/"
starting_date = parser.parse(str(year)).replace(month=1, day=1, hour=0, second=0, minute=0)
while starting_date.weekday() != 0:
    starting_date = starting_date + datetime.timedelta(days=1)


position = starting_date
ending_date = starting_date.replace(year=year + 1)
index = 1
while position.year == year:
    file_path = base_path + local_path + f"Week {index} - {year}.md"
    starting_date = position
    ending_date = position + datetime.timedelta(days=6)
    position = position + datetime.timedelta(days=7)
    index += 1
    if (position < datetime.datetime.now() + datetime.timedelta(days=2)):
        continue
    shutil.copyfile(base_path + template_path, file_path)


    with open(file_path, "r") as f:
        contents = f.readlines()

    contents.insert(6, f"## [[{starting_date.strftime('%-m-%-d-%Y')}]] - [[{ending_date.strftime('%-m-%-d-%Y')}]]\n")

    with open(file_path, "w") as f:
        contents = "".join(contents)
        f.write(contents)
    
