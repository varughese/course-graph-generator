import pickle, json
from pitt_course import PittCourse

def pickleLoader(pklFile):
	try:
		while True:
			yield pickle.load(pklFile)
	except EOFError:
		pass

graph = {
	"nodes": [],
	"links": []
}

with open('courses.pkl', 'rb') as input:
	for course in pickleLoader(input):
		graph["nodes"].append(course.__dict__)
		for prereq in course.prereqs:
			graph["links"].append({"source": prereq, "target": course.id})
		
with open('courses.json', 'w') as outfile:
    json.dump(graph, outfile)