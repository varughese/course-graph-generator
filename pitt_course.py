class PittCourse():
	def __init__(self, id, prereqs, description):
		self.id = id
		self.prereqs = prereqs
		self.description = description
	
	def __str__(self):
		return "{} \nPrereqs: {} \nDescription: {}".format(self.id, self.prereqs, self.description)