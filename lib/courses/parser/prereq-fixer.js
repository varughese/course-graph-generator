const readline = require('readline');
const { parse } = require('./parser'); 

const ask = (rl, query) => new Promise(resolve => rl.question(query, resolve));

async function fetchInput() {
	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout
	});
	const input = await ask(rl, "> ");
	rl.close();
	return input
}

function prereqsFailedToParse(course) {
	return course && course.reqs && course.reqs.tree == null && course.reqs.text != '';
}

// Overwrites and reparses a prereq string
async function promptAndFixCourse(course) {
	if (prereqsFailedToParse(course)) {
		do {
			const text = course.reqs.text;
			console.log(course.id + ": " + text);
			const userInput = await fetchInput();
			if ("skip" === userInput || "" === userInput) {
				return 1;
			}
			const newPrereqStr = userInput.trim();
			try {
				course.reqs.tree = parse(newPrereqStr);
				promptUser = false;
			} catch (err) {
				course.reqs.tree = null
				console.log("Did not work");
			}
		} while(course.reqs.tree === null);
	}
	return 0;
}

module.exports = {
	prereqsFailedToParse,
	fetchInput,
	promptAndFixCourse
}