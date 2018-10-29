

class Article:
	def __init__ (self, articleName, authorName, link, date, issueNum):
		self.articleName = articleName
		self.authorName = authorName
		self.link = link
		self.date = date
		self.issueNum = issueNum

	def __str__(self):
		return f'Article: [name: "{self.articleName}", issueNum: {self.issueNum}, authorName: "{self.authorName}", link: "{self.link}", date: "{self.date}"'

	def __repr__(self):
		return self.__str__()	