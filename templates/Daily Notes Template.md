---
tags:
  - dailies
adderall: false
alcohol: false
caffeine: false
cooked: false
exercise: false
gaming: false
weed: false
meditate: false
rating: 
stress: 
motivation: 
location: 
version: 1.0.6
---
<%*
// Relevant variables to all sections
let weeklyItemsFile = "Personal/Bullet Journal Meta/Schedule/Weekly.md"
let weeklyItemsText = await this.app.vault.read(tp.file.find_tfile(weeklyItemsFile))

let monthlyItemsFile = "Personal/Bullet Journal Meta/Schedule/Monthly.md"
let monthlyItemsText = await this.app.vault.read(tp.file.find_tfile(monthlyItemsFile))

let yearlyItemsFile = "Personal/Bullet Journal Meta/Schedule/Yearly.md"
let yearlyItemsText = await this.app.vault.read(tp.file.find_tfile(yearlyItemsFile))

let fileDate = moment(tp.file.title)

function getDataFromTable(rawTable, rowName, columnName) {
	let columnMapping = {}
	let rows = rawTable.split("\n")

	// We do the second row as there's an empty space
	let headerRow = rows[1].split("|")
	for (let i = 0; i < headerRow.length; i++) {
		columnMapping[headerRow[i].trim()] = i
	}

	for (const row of rows) {

		if (!row) {
			continue
		}
		let columns = row.split("|")
		let rowIndex = columns[1].trim()

		if (rowIndex === rowName) {
			let result = columns[columnMapping[columnName]]
			if (result) {
				return result.trim().split("<br>")
			}
			return ""
		}
	}
	return ""
}

// All of the date stuff
let currentWeekday = fileDate.format("dddd")
let currentDay = fileDate.format("D")
let currentMonth = fileDate.format("MMMM")

let weeklyItemsToDo = getDataFromTable(weeklyItemsText, currentWeekday, "To Do")
let weeklyItemsWorkToDo = getDataFromTable(weeklyItemsText, currentWeekday, "Work To Do")
let monthlyItems = getDataFromTable(monthlyItemsText, currentDay, "Item")
let yearlyItems = getDataFromTable(yearlyItemsText, currentDay, currentMonth)


let allTodos = weeklyItemsToDo.concat(monthlyItems, yearlyItems).filter(r => r.trim())
let workTodos = weeklyItemsWorkToDo.filter(r => r.trim())

%>
#### [[<% fileDate = moment(tp.file.title, 'M-D-YYYY').startOf('month').format('M - MMMM YYYY') %>]]
<%*
// TODO: Do I really need / want this?
let currentDate = moment(tp.file.title).startOf('day')
let counterStart = moment(currentDate).startOf('year')
// Move the counter along until we get to the first Monday
while (counterStart.day() !== 1) {
	counterStart.add(1, "d")
}
let index = 0
while (counterStart <= currentDate) {
	index = index + 1
	counterStart.add(7, "d")
}
tR += "[[ Week " + index.toString() + " - " + currentDate.year().toString() + "]]"

%>

# Notes
- 

# To Do
<%*
let relevantTodos = weeklyItemsToDo.concat(monthlyItems, yearlyItems).filter(r => r.trim())
if (relevantTodos.length > 0) {
	for (const todo of relevantTodos) {
		// This IF is carrying the fact that we will have empty strings in the list
		if (todo) {
			tR += "- [ ] #recurring " + todo + "\n"
		}
	}
} else {
	tR += "- [ ] "
}
%>
<%*
let day = moment(tp.file.title).day()
if (day !== 6 && day !== 0) {
	tR += "\n# Work Notes\n";
	tR += "- \n\n\n";
	tR += "# Work To Do\n";
	for (const todo of weeklyItemsWorkToDo) {
		tR += "- [ ] #recurring " + todo + "\n"
	}
}
%>

# Meals
> breakfast:: [[Morning Shake]]
> lunch:: 
> dinner:: 
> snacks:: 