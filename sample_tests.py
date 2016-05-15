import unittest
import datetime
from prettyunit import PrettyUnit


class BaseTest1(unittest.TestCase):
	"""
	Our basic test class
	"""

	def test_pass1(self):
		"""
		built to pass 1
		"""
		f = 4
		self.assertEqual(f, 4)

	@unittest.skip("WIPPPPPPP")
	def test_skip(self):
		"""
		built to pass 2
		"""
		f = 5
		self.assertEqual(f, 5)


class BaseTest2(unittest.TestCase):
	"""
	Our basic test class
	"""


	def test_fail(self):
		"""
		built to pass 3
		"""
		f = 6
		self.assertEqual(f, 5, "did I fail?")

	def test_error(self):
		"""
		built to pass 3
		"""
		f = a
		self.assertEqual(f, 5, "did I error?")






if __name__ == '__main__':
	PU = PrettyUnit()
	# Create test suite
	name, suite = PU.suite("test_suite", BaseTest1, BaseTest2)

	# Start tests
	timestamp = datetime.datetime.now()
	results = unittest.TextTestRunner().run(suite)

	# Populate UC dictionary and generate json
	PU.populateJson(name, suite._tests)
	PU.addResultsJson(results, timestamp)
	json_results = PU.generateJson()
	print json_results


