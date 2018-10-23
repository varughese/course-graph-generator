from bs4 import BeautifulSoup
import requests
import json
import pickle
from pitt_course import PittCourse

URL = "http://courses.sci.pitt.edu"
res = requests.get(URL + "/courses")

class PittScrapedCourse(PittCourse):
	def __init__(self, href):
		self.href = href
		self.id = href[14:]
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
			self.prereqs = [cs_courses[a.attrs["href"]] for a in prereqs if a.attrs["href"] in cs_courses]

	def toSimple(self):
		return PittCourse(self.id, self.prereqs, self.description)

	def __str__(self):
		return super().__str__()

	def __repr__(self):
		return "<PittScrapedCourse {}>".format(self.id) 


soup = BeautifulSoup(res.content, "html.parser")
courses = soup.find_all("li", class_="course computer-science")

hrefs = [li.find("a").attrs["href"] for li in courses]
cs_courses = dict([(href[14:], PittScrapedCourse(href)) for href in hrefs])
for href, course in cs_courses.items():
	course.hydratePreqs(cs_courses)


with open('courses.pkl', 'wb') as output:
	for href, course in cs_courses.items():
		pickle.dump(course.toSimple(), output, pickle.HIGHEST_PROTOCOL)