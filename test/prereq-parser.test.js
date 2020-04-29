const parse = require("../lib/courses/parser/prereq-parser");
const { prereqsFailedToParse } = require("../lib/courses/parser/prereq-fixer");


test("properly sets prereq tree", () => {
	const course = {
		id: "CS1501",
		prereq: ["PREQ: CS0445 (MIN GRADE C)"]
	}
	const parsed = parse(course);
	expect(parsed).toBe(0);
	expect(course.reqs).toEqual({
		text: "PREQ: CS0445 (MIN GRADE C)",
		tree: "CS0445"
	});
})

test("properly sets prereq tree to null if cannot parse string", () => {
	const course = {
		id: "CS1501",
		prereq: ["PREWRONGQ: CS0445 (MIN GRADE C)"]
	}
	const parsed = parse(course);
	expect(parsed).toBe(1);
	expect(course.reqs).toEqual({
		text: "PREWRONGQ: CS0445 (MIN GRADE C)",
		tree: null
	});
})

test("prereqsFailedToParse correctly detects misinterpreted parsed tree", () => {
	const course = {
		id: "MING1555",
		reqs: {
			text: "This is messed up",
			tree: null
		}
	}
	
	expect(prereqsFailedToParse(course)).toBe(true);
	course.reqs.text = '';
	expect(prereqsFailedToParse(course)).toBe(false);
});