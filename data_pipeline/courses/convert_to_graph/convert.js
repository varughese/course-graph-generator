const fs = require("fs").promises;
const path = require("path");

const TERM = 2201

const filePath = path.join("..", "scraped", ""+TERM, "course_data-parsed.json");

function getSubjectFromCourseId(id) {
	return id.substring(0, id.length - 4);
}

function getCourse(allCourses, id) {
	const subject = getSubjectFromCourseId(id); 
	return allCourses[subject][id];
}

function simplifyTree(tree) {
	if (tree.or) {
		tree
	} else if (tree.and) {

	}
}

function convertCourses(allCourses, courses) {
	const nodes = [];
	const links = [];
	for (const id in courses) {
		const course = courses[id];
		simplifyTree(allCourses, course.reqs.prereq)
		simplifyTree(allCourses, course.reqs.coreq)
	}
}

// Each major is going to have its own graph.
async function convertAllCourses() {
	const allCourses = JSON.parse(await fs.readFile(filePath))
	const subjects = ["CS"] //Object.keys(allCourses);
	const graphs = {};
	subjects.forEach(subject => {
		const courses = allCourses[subject];
		graphs[subject] = convertCourses(allCourses, courses);
	});
}
convertAllCourses();