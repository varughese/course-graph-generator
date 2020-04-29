const parse = require("../lib/courses/prereq_parser/prereq-parser");


test("properly sets prereq tree", () => {
	const course = {
		id: "CS1501",
		prereq: ["PREQ: CS0445 (MIN GRADE C)"]
	}
	const parsed = parse(course);
	expect(parsed.reqs).toEqual({
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
	expect(parsed.reqs).toEqual({
		text: "PREWRONGQ: CS0445 (MIN GRADE C)",
		tree: null
	});
  })