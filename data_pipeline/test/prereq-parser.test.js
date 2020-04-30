const pegjsparser = require("../courses/parser/parser").parse;
const parse = require("../courses/parser/prereq-parser");
const { prereqsFailedToParse } = require("../courses/parser/prereq-fixer");

test("peg js parser is correct", () => {
	const cases = [
		["PREQ: BIOENG 1310 and MATH 0240 and MATH 0290 CREQ: cs1504", {
			"prereq": {
			   "and": [
				  "BIOENG1310",
				  "MATH0240",
				  "MATH0290"
			   ]
			},
			"coreq": "CS1504"
		}],
		["PREQ: BIOENG 1310; PLAN bioengineer ", {
			"prereq": "BIOENG1310",
			"coreq": null
		}],
	].forEach(([text, output]) => expect(pegjsparser(text)).toEqual(output))
})

test("properly sets prereq tree", () => {
	const course = {
		id: "CS1501",
		prereq: ["PREQ: CS0445 (MIN GRADE C)"]
	}
	const parsed = parse(course);
	expect(parsed).toBe(0);
	expect(course.reqs).toEqual({
		text: "PREQ: CS0445 (MIN GRADE C)",
		tree: {
			"coreq": null,
			"prereq": "CS0445",
		}
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
			text: "PLAN Engineering",
			tree: null
		}
	}
	
	expect(prereqsFailedToParse(course)).toBe(false);
	course.reqs.text = '';
	expect(prereqsFailedToParse(course)).toBe(false);
	course.reqs.text = 'PREQ: failed to parse';
	expect(prereqsFailedToParse(course)).toBe(true);
});