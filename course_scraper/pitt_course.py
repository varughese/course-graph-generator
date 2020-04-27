class PittCourse():
	def __init__(self, id, prereqs, description, href):
		self.id = id
		self.prereqs = prereqs
		self.description = description
		self.href = href
	
	def __str__(self):
		return "{} \nPrereqs: {} \nDescription: {}".format(self.id, self.prereqs, self.description)

	def __repr__(self):
		return "<PittCourse {}>".format(self.id)