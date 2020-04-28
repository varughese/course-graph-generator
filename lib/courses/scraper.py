import course as course_util
import json
from multiprocessing import Pool, Manager
import sys   
import os

# We have to do this because the beautiful soup xml trees are big
sys.setrecursionlimit(10000) 

class Course:
	def __init__(self, id, className, major, classNumber, prereq, recitation, credit, description, coreq):
		self.id = id
		self.className = className
		self.major = major
		self.classNumber = classNumber
		self.prereq = prereq
		self.recitation = recitation
		self.credits = credit
		self.description = description
		self.coreq = coreq

	def __str__(self):
		return str(self.id + ": " + self.className)

def serialize_course(obj):
   if isinstance(obj, Course):
	   serial = json.dumps(obj.__dict__, sort_keys=True, indent=4)
	   return serial
   else:
	   raise TypeError ("Type not serializable")


def scrape_course(course_map, course):
	try: 
		current = course
		classNumber = current.number
		if int(classNumber[0:4]) >= 2000: return
		className = current.title
		major = current.subject
		id = major + "" + classNumber
		prereq = []
		recitation = False
		credits = 0
		description = ""
		coreq = []

		foundLecture = False
		for section in current.sections:
			typ = section.section_type
			if typ == 'REC' or typ == 'LAB':
				recitation = True
				continue
			elif typ == "LEC" or typ == "PRA" or typ == "SEM" or typ == "CLB" or typ == "CLN" or typ == "WRK" or typ == "CLQ" or typ == "MSM":  
				if foundLecture: continue 
				
				try:
					extra = section.extra_details
				except:
					print(id)
					raise
				if extra == None: continue
				credits = extra['units']
				description = extra['description']
				if 'preq' in extra:
					
					prereq.append(extra['preq'])

				foundLecture = True
			elif typ == "INT" or typ == "IND" or typ == "DIR" or typ == "THE":
				continue
				#ignore these types
			else:
				print("diff type error: " + typ + "_" + id)

		course_map[id] = Course(id,className,major, classNumber, prereq, recitation, str(credits), description, coreq)
		print(id)
	except Exception as error:
		print(error)
		raise

def scrape_subject_by_term(term, subj):
	classes = []
	manager = Manager()
	course_map = manager.dict()
	p = manager.Pool(10)
	print(subj)
	
	class_dict = course_util.get_term_courses(term, subj).get_course_dict()
	for course in class_dict.values():
		p.apply_async(scrape_course, args=(course_map, course))

	p.close()
	p.join()
	return dict(course_map)


output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scraped')

def scrape_term(term):
	term = str(term)
	data = {}
	output_path_term = os.path.join(output_path, term)
	os.makedirs(output_path_term, exist_ok=True)
	for subject in SUBJECTS_TO_SCRAPE:
		output_path_subject = os.path.join(output_path_term, "{}.json".format(subject))
		if os.path.isfile(output_path_subject):
			continue
		print("Scraping", subject)
		data[subject] = {}
		for course_id, course in scrape_subject_by_term(term, subject).items():
			data[subject][course_id] = course.__dict__

		to_write = json.dumps(data, default=serialize_course, sort_keys=True, indent=4)
		f = open(output_path_subject,"w")
		f.write(to_write)
		f.close()


SUBJECTS_TO_SCRAPE = course_util.undergrad_subjects
scrape_term(2201)