const { parse } = require('./parser'); 

// Returns 0 if succesfully parsed, 1 if unsuccesful. Mutates the course object passed in.
module.exports = function(course) {
	// { prereq: ["PREQ: CS556 "] }
	const prereqString =  Array.isArray(course.prereq) ? course.prereq[0] || '' : course.prereq;
	course.reqs = {
		text: prereqString,
		tree: null
	}
	try {
		course.reqs.tree = parse(prereqString);
		return 0;
	} catch (err) {
		course.reqs.tree = null
		return 1;
	}
}