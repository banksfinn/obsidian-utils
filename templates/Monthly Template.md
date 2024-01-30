---
tags:
  - monthly
version: 1.1.1
---
<< [[<% fileDate = "Personal/Bullet Journal/" + moment(tp.file.title, "M - MMMM YYYY").subtract(1, "month").format("YYYY") + "/Monthly/" + moment(tp.file.title, "M - MMMM YYYY").subtract(1, "month").startOf("month").format('M - MMMM YYYY') %>|Previous Month]] | [[<% fileDate = "Personal/Bullet Journal/" + moment(tp.file.title, "M - MMMM YYYY").add(1, "month").format("YYYY") + "/Monthly/" + moment(tp.file.title, "M - MMMM YYYY").add(1, "month").startOf("month").format('M - MMMM YYYY') %>|Next Month]] >>

# Summary

# Goals


```dataviewjs
// CONSTANTS
const bounds = 2
const criticalTag = "#monthly"
const templateName = "Monthly Template"

const sectionToggle = {
	"tags": true,
	"propertyGraph": true,
	"ratingGraph": true,
	"incompleteTasks": true,
	"mealsTable": false,
}

function getMinAndMaxDate(datePadding) {
	let minimumGraphDate = moment(dv.current().file.name, "M - MMMM YYYY").startOf("month")
	if (datePadding) {
		minimumGraphDate = minimumGraphDate.subtract("days", datePadding)
	}

	let maximumGraphDate = moment(dv.current().file.name, "M - MMMM YYYY").endOf("month")

	if (datePadding) {
		maximumGraphDate = maximumGraphDate.add("days", datePadding)
	}
	
	if (maximumGraphDate > moment()) {
		maximumGraphDate = moment()
	}
	// TODO!
	// If datePadding is 0, we don't include extra
	return {
		"min": minimumGraphDate,
		"max": maximumGraphDate
	}
}

// Everything else below this should be the same across
// Weekly, Monthly, and Year

// If graph bounds is 0, then we do nothing
function generateRelevantPages(datePadding) {
	const dateData = getMinAndMaxDate(datePadding)
	
	let relevantPages = dv.pages('#dailies').where(p => p.file.name !== "Daily Notes Template" && moment(p.file.name) >= dateData["min"] && moment(p.file.name) <= dateData["max"])
	
	// Sort the Pages
	relevantPages.values.sort((a, b) =>  {
	return moment(a.file.name, "MM-DD-YYYY") - moment(b.file.name, "MM-DD-YYYY")
	})
	return relevantPages
}

// We do this to allow us a little preview here
let relevantPages = []
let relevantGraphPages = []
if (dv.current().file.name !== templateName) {
	relevantPages = generateRelevantPages(0)
	relevantGraphPages = generateRelevantPages(bounds)
}

// Constants
const tags = {
	"major": {
		"tag": "#major",
		"title": "Major"
	},
	"minor": {
		"tag": "#minor",
		"title": "Minor"
	},
	"highs": {
		"tag": "#highs",
		"title": "Highs"
	},
	"lows": {
		"tag": "#lows",
		"title": "Lows"
	},
	"learnings": {
		"tag": "#learnings",
		"title": "Learnings"
	},
	"health": {
		"tag": "#health",
		"title": "Health"
	},
}

let propertyLookup = {
	"adderall": {
		"title": "Adderall",
		"type": "binary",
		"field": "adderall",
		"color": "11, 129, 162"
	},
	"alcohol": {
		"title": "Alcohol",
		"type": "binary",
		"field": "alcohol",
		"color": "130, 85, 171"
	},
	"caffeine": {
		"title": "Caffeine",
		"type": "binary",
		"field": "caffeine",
		"color": "209, 129, 67",
	},
	"cooked": {
		"title": "Cooked",
		"type": "binary",
		"field": "cooked",
		"color": '147, 156, 33',
	},
	"exercise": {
		"title": "Exercise",
		"type": "binary",
		"field": "exercise",
		"color": '158, 46, 72',
	},
	"gaming": {
		"title": "Gaming",
		"type": "binary",
		"field": "gaming",
		"color": "47, 204, 12",
	},
	"weed": {
		"title": "Weed",
		"type": "binary",
		"field": "weed",
		"color": '73, 112, 87',
	},
	"meditate": {
		"title": "Meditate",
		"type": "binary",
		"field": "meditate",
		"color": "45, 48, 145",
	},
	"rating": {
		"title": "Rating",
		"type": "rating",
		"field": "rating",
		"color": "20, 204, 183",
	},
	"stress": {
		"title": "Stress",
		"type": "rating",
		"field": "stress",
		"color": "199, 46, 46",
	},
	"motivation": {
		"title": "Motivation",
		"type": "rating",
		"field": "motivation",
		"color": "59, 13, 212",
	}
}

// Shared Functions
function parseStringRating(rating) {
	if (!rating) {
		return 0
	}
	return parseFloat(rating.split("/")[0])
}

// Check if the integer is within the bounds of the array
function integerWithinBounds(i, array) {
	if (i < 0) {
		return false
	}
	if (i > array.length - 1) {
		return false
	}
	return true
}

function convertDataToDataset(property) {
	const borderColor = "color" in propertyLookup[property] ? "rgba(" + propertyLookup[property]["color"] + ",1)" : 'rgba(255, 99, 132, 1)'
	const backgroundColor = "color" in propertyLookup[property] ? "rgba(" + propertyLookup[property]["color"] + ",0.2)" : 'rgba(255, 99, 132, 1)'
	return {
		label: propertyLookup[property]["title"],
		data: averagedData["properties"][property],
		type: 'line',
		backgroundColor: [ backgroundColor ], 
		borderColor: [ borderColor ], 
		borderWidth: 1 ,
		tension: 0.3,
	}
}

function generatePropertyAndRatingData() {
	const averagedData = {
		"names": [],
		"properties": {}
	}
	
	for (const property of Object.keys(propertyLookup)) {
		averagedData["properties"][property] = []
	}
	for (let i = 0; i < relevantGraphPages.length; i++) {
		const addItem = !bounds || (i >= bounds && i <= relevantGraphPages.length - bounds)
		for (const property of Object.keys(propertyLookup)) {
			let tempSum = 0
			if (bounds) {
				for (let j = -bounds; j <= bounds; j++) {
					if (integerWithinBounds(i + j, relevantGraphPages)) {
						const field = propertyLookup[property]["field"]
						if (propertyLookup[property]["type"] === "binary") {
							tempSum += relevantGraphPages[i + j][field] ? 1 : 0
						} else if (propertyLookup[property]["type"] === "rating") {
							tempSum += parseStringRating(relevantGraphPages[i + j][field]) ?? "0"
						}
					}
				}
			} else {
				const field = propertyLookup[property]["field"]
				if (propertyLookup[property]["type"] === "binary") {
					tempSum += relevantGraphPages[i][field] ? 1 : 0
				} else if (propertyLookup[property]["type"] === "rating") {
					tempSum += parseStringRating(relevantGraphPages[i][field]) ?? "0"
				}
			}
	
			if (addItem) {
				averagedData["properties"][property].push(tempSum)
			}
		}
		if (addItem) {
			averagedData["names"].push(relevantGraphPages[i].file.name)
		}
	}
	return averagedData
}

// Tag Information
if (sectionToggle["tags"]) {
	dv.header(1, "Tags")
	const data = {}
	for (const tag of Object.keys(tags)) {
		data[tag] = []
	}
	
	for (const page of relevantPages) {
		for (const item of page.file.lists.values) {
			for (const tag of Object.keys(tags)) {
				if (item.tags.includes(tags[tag]["tag"]) && (!criticalTag || item.tags.includes(criticalTag))) {
					data[tag].push({
						"item": item,
						"name": page.file.name
					})
				}
			}
		}
	}
	for (const tag of Object.keys(tags)) {
		let header = dv.header(2, tags[tag]["title"])
		let results = []
		for (const i of data[tag]) {
			results.push(["- [[" + i["name"] + "]]: " + i["item"].text])
	
		}
		dv.table([header], results)
		dv.header(3, "")
	}
}

if (sectionToggle["incompleteTasks"] && relevantPages.length) {
	dv.header(1, "Incomplete Tasks")
	dv.taskList(relevantPages.file.tasks.where(t => !t.completed && (t.header?.subpath ?? "").includes("To Do")))
}


let averagedData = {}
if (sectionToggle["propertyGraph"] || sectionToggle["ratingGraph"]) {
	averagedData = generatePropertyAndRatingData()
}

if (sectionToggle["propertyGraph"]) {
	dv.header(1, "Property Graph")
	
	const propertyDatasets = Object.keys(propertyLookup).filter((key) => propertyLookup[key]["type"] === "binary").map((key) => convertDataToDataset(key))
	
	const propertyChartData = {
		data: {
			labels: averagedData["names"],
			datasets: propertyDatasets
		}
	}
	window.renderChart(propertyChartData, this.container);
}

if (sectionToggle["ratingGraph"]) {
	const ratingDatasets = Object.keys(propertyLookup).filter((key) => propertyLookup[key]["type"] === "rating").map((key) => convertDataToDataset(key))
	
	const ratingChartData = {
		data: {
			labels: averagedData["names"],
			datasets: ratingDatasets
		}
	}
	window.renderChart(ratingChartData, this.container);
}

if (sectionToggle["mealsTable"]) {
	dv.header(1, "Meals")
	let mealsRes = []
	for (const p of relevantPages) {
		mealsRes.push([
			"[[" + p.file.name + "]]",
			p.breakfast,
			p.lunch,
			p.dinner])
	}
	const mealsHeaders = ["Date", "Breakfast", "Lunch", "Dinner"]
	dv.table(mealsHeaders, mealsRes)
}
```