class OutOfUserException(Exception):
	"""this exception is thrown when the number of users to be added is exhausted."""
	def __init__(self, count, limit, message='users exhausted when adding'):
		super(OutOfUserException, self).__init__()
		self.message = message
		self.limit = limit
		self.count = count

	def __str__(self):
		"""Thi invokes a call to the str method when this object is printed like a string."""
		return self.message
		