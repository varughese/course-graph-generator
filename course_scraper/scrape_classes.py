from bs4 import BeautifulSoup
import requests
import json
import pickle
from pitt_course import PittCourse

URL = "http://courses.sci.pitt.edu"
res = requests.get(URL + "/courses")

def hrefToId(href):
	id = ""
	for c in href[14:]:
		if len(id) > 2 and id[-1] == '-' and c == '0':
			continue
		else:
			id += c
	return id

class PittScrapedCourse(PittCourse):
	def __init__(self, href):
		self.href = href
		self.id = hrefToId(href)
		print("Loading {}".format(self.id))
		self.res = requests.get(URL + self.href)
		self.soup = BeautifulSoup(self.res.content, "html.parser")
		self.getDescription()

	def getDescription(self):
		p = self.soup.select("#main > p")
		self.description = p[0].contents[0].strip()

	def hydratePreqs(self, cs_courses):
		prereqs = self.soup.select("#main > ul li a")
		if not prereqs:
			self.prereqs = []
		else:
			self.prereqs = [hrefToId(a.attrs["href"]) for a in prereqs]
			print(self.prereqs)

	def toSimple(self):
		return PittCourse(self.id, self.prereqs, self.description, self.href)

	def __str__(self):
		return super().__str__()

	def __repr__(self):
		return "<PittScrapedCourse {}>".format(self.id) 


soup = BeautifulSoup(res.content, "html.parser")
courses = soup.find_all("li", class_="course computer-science")

hrefs = [li.find("a").attrs["href"] for li in courses]
cs_courses = dict([(hrefToId(href), PittScrapedCourse(href)) for href in hrefs])

for href, course in cs_courses.items():
	course.hydratePreqs(cs_courses)
	print(str(course))

with open('courses.pkl', 'wb') as output:
	for href, course in cs_courses.items():
		print(str(course))
		pickle.dump(course.toSimple(), output, pickle.HIGHEST_PROTOCOL)