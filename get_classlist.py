from bs4 import BeautifulSoup
import requests

URL = "http://courses.sci.pitt.edu"
res = requests.get(URL + "/courses")

class PittCourse:
	def __init__(self, href):
		self.href = href
		self.id = href[14:]

	def hydratePreqs(self, cs_courses):
		print("GETTING {}".format(self.id))
		res = requests.get(URL + self.href)
		soup = BeautifulSoup(res.content, "html.parser")
		prereqs = soup.select("#main > ul li a")
		if not prereqs:
			self.prereqs = []
		else:
			self.prereqs = [cs_courses[a.attrs["href"]] for a in prereqs if a.attrs["href"] in cs_courses]
	
	def __repr__(self):
		return "<{}>".format(self.id) 

soup = BeautifulSoup(res.content, "html.parser")
courses = soup.find_all("li", class_="course computer-science")

hrefs = [li.find("a").attrs["href"] for li in courses]
cs_courses = dict([(href, PittCourse(href)) for href in hrefs])
for href, course in cs_courses.items():
	course.hydratePreqs(cs_courses)

print(cs_courses)
