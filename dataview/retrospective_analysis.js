// ---------------------------------------------------
// ------------------ CONSTANTS ----------------------
// ---------------------------------------------------


// This variable changes how properties are computed on a given day. With a bounds
// of 0, we look at a single day exlusively (which has either a 1 or a 0)/
// With a bounds of 1, we look at the days on either side as well, so the range is from 3 to 0
// This smooths out the graph, and provides a better sense of overall trends for larger
// date ranges
const bounds = 0
// Use a tag here if you want to filter all lines by this. For example, I use the tags #monthly
// and #yearly to indicate if I want those line items to bubble up to my monthly / yearly retro
const criticalTag = ""
// What the name of the template is that this file is in. This just makes it a little prettier
// in the template folder by not failing the queries
const templateName = "Weekly Template"

// Use this to toggle tags, properties, ratings, incomplete tasks, and meals
const sectionToggle = {
	"tags": true,
	"propertyGraph": true,
	"ratingGraph": true,
	"incompleteTasks": true,
	"mealsTable": true,
}

// Styling on the various tags and properties I track
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

// This should be overwritten based on the template using it. The input should be the amount of
// extra padding to add on either side of the given date, and the output should be the minimum
// and maximum dates *given the date of the current file name*.
function getMinAndMaxDate(datePadding) {
	let weekNumber = parseInt(dv.current().file.name.split("Week ")[1].split(" -")[0])
	let year = parseInt(dv.current().file.name.split(" - ")[1])
	let startingDate = moment().set("year", year).startOf("year")
	while (startingDate.day() !== 1) {
		startingDate.add(1, "d")
	}

	for (let i = 1; i < weekNumber; i++) {
		startingDate.add(7, "d")
	}

	let minimumGraphDate = startingDate.clone()
	let maximumGraphDate = startingDate.clone().add(6, "d")

	if (datePadding) {
		minimumGraphDate = minimumGraphDate.subtract("days", datePadding)
		maximumGraphDate = maximumGraphDate.add("days", datePadding)
	}
	return {
		"min": minimumGraphDate,
		"max": maximumGraphDate
	}
}

// Everything else below this should be the same across all systems

// Generate the relevant pages to both sections
function generateRelevantPages(datePadding) {
	const dateData = getMinAndMaxDate(datePadding)

	let relevantPages = dv.pages('#dailies').where(p => p.file.name !== "Daily Notes Template" && moment(p.file.name) >= dateData["min"] && moment(p.file.name) <= dateData["max"])

	// Sort the Pages
	relevantPages.values.sort((a, b) => {
		return moment(a.file.name, "MM-DD-YYYY") - moment(b.file.name, "MM-DD-YYYY")
	})
	return relevantPages
}

// We do this to allow us a little preview in the template here
let relevantPages = []
let relevantGraphPages = []
if (dv.current().file.name !== templateName) {
	relevantPages = generateRelevantPages(0)
	relevantGraphPages = generateRelevantPages(bounds)
}


// Convert a "3/5" to the number
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

// Convert a given property to its relevant graph data
function convertPropertyDataToGraphData(property) {
	const borderColor = "color" in propertyLookup[property] ? "rgba(" + propertyLookup[property]["color"] + ",1)" : 'rgba(255, 99, 132, 1)'
	const backgroundColor = "color" in propertyLookup[property] ? "rgba(" + propertyLookup[property]["color"] + ",0.2)" : 'rgba(255, 99, 132, 1)'
	return {
		label: propertyLookup[property]["title"],
		data: averagedData["properties"][property],
		type: 'line',
		backgroundColor: [backgroundColor],
		borderColor: [borderColor],
		borderWidth: 1,
		tension: 0.3,
	}
}

// Generate the relevant property and rating data
function generatePropertyAndRatingData() {
	const averagedData = {
		"names": [],
		"properties": {}
	}

	// Seed the initial dictionary
	for (const property of Object.keys(propertyLookup)) {
		averagedData["properties"][property] = []
	}

	// Loop through every page
	for (let i = 0; i < relevantGraphPages.length; i++) {
		// Check if we actually want to add the item to the dataset
		// We don't want to do this if this is something we want to use for calculation but
		// not display
		const addItem = !bounds || (i >= bounds && i <= relevantGraphPages.length - bounds)
		// For each property, loop through the page (and nearby pages if relevant)
		// and compute the sum
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

// Display Tag Information
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

// Display Incomplete Tasks
if (sectionToggle["incompleteTasks"] && relevantPages.length) {
	dv.header(1, "Incomplete Tasks")
	dv.taskList(relevantPages.file.tasks.where(t => !t.completed && (t.header?.subpath ?? "").includes("To Do")))
}


// Generate averaged data if we want either of these graphs
// Since this function generates them both at the same time, we have the if
let averagedData = {}
if (sectionToggle["propertyGraph"] || sectionToggle["ratingGraph"]) {
	averagedData = generatePropertyAndRatingData()
}

// Show the property graph
if (sectionToggle["propertyGraph"]) {
	dv.header(1, "Property Graph")

	const propertyDatasets = Object.keys(propertyLookup).filter((key) => propertyLookup[key]["type"] === "binary").map((key) => convertPropertyDataToGraphData(key))

	const propertyChartData = {
		data: {
			labels: averagedData["names"],
			datasets: propertyDatasets
		}
	}
	window.renderChart(propertyChartData, this.container);
}

// Show the rating graph
if (sectionToggle["ratingGraph"]) {
	const ratingDatasets = Object.keys(propertyLookup).filter((key) => propertyLookup[key]["type"] === "rating").map((key) => convertPropertyDataToGraphData(key))

	const ratingChartData = {
		data: {
			labels: averagedData["names"],
			datasets: ratingDatasets
		}
	}
	window.renderChart(ratingChartData, this.container);
}

// Show meals if relevant
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
