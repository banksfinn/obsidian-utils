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
let recurringTodosFileName = "Personal/Bullet Journal Tracker/Schedule/Recurring Tasks.md"
let recurringWorkFileName = "Personal/Bullet Journal Tracker/Schedule/Recurring Work.md"
let exerciseFileName = "Personal/Bullet Journal Tracker/Schedule/Exercise Schedule.md"

let relevantDate = moment(tp.file.title).format("dddd")

function getTodosFromFile(text, tag) {
	let todos = []
	let sections = text.split("[[" + tp.file.title + "]]\n")
	if (!sections.length) {
		return []
	}
	for (const section of sections.slice(1)) {
		let currentSection = section.split("\n\n")[0]
		// Split on new line
		let items = currentSection.split("\n")
		for (const item of items) {
			// If it is a todo, add
			let parsedItem = item.trim()
			if (item.includes("- ")) {
				todos.push("- [ ] " + tag + " " + parsedItem.slice(2) + "\n")
			}
		}
	}
	return todos
}

function grabRecurringTodos(text, tag, date) {
	let todos = []
	let splitText = text.split(date)
	// If we don't show the date, return nothing
	if (!splitText || splitText.length < 2) {
		return todos
	}
	// Grab the second portion (aka after the date), split by double new line
	let relevantSection = splitText[1].split("\n\n")[0] ?? ""
	// Skip the first element
	for (const item of relevantSection.split("\n").slice(1)) {
		todos.push(item.slice(0, 6) + tag + " " + item.slice(6) + "\n")
	}
	return todos
}

function grabExercise(text, date) {
	let exercise = []
	let startingDate = moment(tp.file.title).format("dddd")
	let endingDate = moment(tp.file.title).add(1, "d").format("dddd")
	let splitText = text.split("# " + startingDate + "\n")
	// If we don't show the date, return nothing
	if (!splitText || splitText.length < 2) {
		return todos
	}

	let p = splitText[1].split("\n\n# " + endingDate)
	return p[0].split("\n\n")
}

let longTermTodos = []
if (moment(tp.file.title).date() > 29) {
	longTermTodos.push("- [ ] #recurring Pay Rent\n")
}

if (moment(tp.file.title).date() === 22) {
	longTermTodos.push("- [ ] #recurring Replace toothbrush head\n")
}

if (moment(tp.file.title).date() === 7 || moment(tp.file.title).date() === 21) {
	longTermTodos.push("- [ ] #recurring Crest whitestrip\n")
}
let nailCleaningDates = [5, 15, 25]
if (nailCleaningDates.includes(moment(tp.file.title).date())) {
	longTermTodos.push("- [ ] #recurring Trim nails\n")
}

if (moment(tp.file.title).date() === moment(tp.file.title).endOf('month').date()) {
	longTermTodos.push("- [ ] #recurring Monthly Recap\n")
}

let updateLinkedInMonths = [1, 7]
if (moment(tp.file.title).date() === 1 && updateLinkedInMonths.includes(moment(tp.file.title).month())) {
	longTermTodos.push("- [ ] #recurring Update LinkedIn\n")
}

// Recurring todos
let recurringTasksFile = tp.file.find_tfile(recurringTodosFileName)
let recurringTasksData = await this.app.vault.read(recurringTasksFile)
let recurringTasks = grabRecurringTodos(recurringTasksData, "#recurring", relevantDate)

// Recurring todos
let exerciseScheduleFile = tp.file.find_tfile(exerciseFileName)
let exerciseScheduleData = await this.app.vault.read(exerciseScheduleFile)
let recurringExercise = grabExercise(exerciseScheduleData, relevantDate)

// Recurring todos
let recurringWorkFile = tp.file.find_tfile(recurringWorkFileName)
let recurringWorkData = await this.app.vault.read(recurringWorkFile)
let recurringWork = grabRecurringTodos(recurringWorkData, "#recurring", relevantDate)

let relevantTodos = recurringTasks.concat(longTermTodos)
let workTodos = recurringWork
%>
#### [[<% fileDate = moment(tp.file.title, 'M-D-YYYY').startOf('month').format('M - MMMM YYYY') %>]]
<< [[<% fileDate = 'Personal/Bullet Journal/' + moment(tp.file.title, 'M-D-YYYY').subtract(1, 'd').format('YYYY') + "/" + moment(tp.file.title, 'M-D-YYYY').subtract(1, 'd').format('M - MMMM') + "/" + moment(tp.file.title, 'M-D-YYYY').subtract(1, 'd').format('M-D-YYYY') %>|Yesterday]] | [[<% fileDate = 'Personal/Bullet Journal/' + moment(tp.file.title, 'M-D-YYYY').add(1, 'd').format('YYYY') + "/" + moment(tp.file.title, 'M-D-YYYY').add(1, 'd').format('M - MMMM') + "/" + moment(tp.file.title, 'M-D-YYYY').add(1, 'd').format('M-D-YYYY') %>|Tomorrow]] >>
<%*
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
if (relevantTodos.length > 0) {
	for (const todo of relevantTodos) {
		tR += todo
	}
} else {
	tR += "- [ ] "
}
%>
<%*
let day = moment(tp.file.title).day()
if (workTodos.length > 0 || (day !== 6 && day !== 0)) {
	tR += "\n# Work Notes\n";
	tR += "- \n\n\n";
	tR += "# Work To Do\n";
	for (const todo of workTodos) {
		tR += todo
	}
}
%>

# Meals
> breakfast:: [[Morning Shake]]
> lunch:: 
> dinner:: 
> snacks:: 