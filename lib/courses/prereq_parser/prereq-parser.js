const { parse } = require('./parser'); 

module.exports = function(course) {
	// { prereq: ["PREQ: CS556 "] }
	const prereqString =  Array.isArray(course.prereq) ? course.prereq[0] || '' : course.prereq;
	course.reqs = {
		text: prereqString,
		tree: null
	}
	try {
		course.reqs.tree = parse(prereqString);
	} catch (err) {
		course.reqs.tree = null
	}
	return course;
}