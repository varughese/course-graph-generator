import pickle
from pitt_course import PittCourse

def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass

with open('courses.pkl', 'rb') as input:
	for course in pickleLoader(input):
		print(course)