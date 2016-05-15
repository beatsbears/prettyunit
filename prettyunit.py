import unittest
import datetime
import json
import socket

class PrettyUnit():
	'''
	A framework to provide usable results for reporting from unittest. 

	Attributes:
		data (dict): A dictionary storing all test that that will eventually be converted into a json str
		MACHINE_NAME (str): A 


	'''

	def __init__(self):
		self.data = {}
		self.seedData()

	def seedData(self):
		'''
		This method is used to gather any non-test-specific information.
		
		Note: This method may be expanded in the future to allow for passing additional attributes to the PrettyUnit instance.
			  However, for now it will only fetch and store the name of the machine the tests are running on.
		'''
		try:
			self.MACHINE_NAME = socket.gethostname()
		except Exception, e:
			print str(e)



	def suite(self, suitename, *testcases):
		'''
		Returns a testsuite object with a name string. If the TestSuite object has not already been defined in the unittest program, this method should be used.

		Args:
			suitename (str): This should be a user provided friendly display name for the test suite.
			*testcases (unittest.TestCase): This will be all instances of the unittest.TestCase class created.
			
		Returns:
			name (str): This just returns the name of the suite that was privided as an arguement.
			suite (unittest.suite.TestSuite):  This returns a newly created TestSuite object which has been populated with all of the test cases.

		Examples:
			name, suite = PrettyUnit.suite("My Test Suite", BaseTest1, BaseTest2, BaseTest3)
		'''
		loader = unittest.TestLoader()
		cases = []
		try:
			for case in testcases:
				cases.append(loader.loadTestsFromTestCase(case))

			test_suite = unittest.TestSuite(cases)
			self.TOTAL_TEST_COUNT = test_suite.countTestCases()
			return (suitename, test_suite)
		except Exception, e:
			print '[!] Test suite generation failed! \n{}'.format(str(e))


	def populateJson(self,testsuite_name,*testcases):
		'''
		Initial json seeding and base creation prior to the results object

		Args:
			testsuite_name (str): This is the name returned by the suite method
			*testcases (list): 

		Returns:
			None

		Examples:



		'''
		# populate known value
		self.data["suite-name"] = testsuite_name
		self.data["server"] = self.MACHINE_NAME
		self.data["test-to-run"] = self.TOTAL_TEST_COUNT	


		tcs = {}
		tn = []
		testnames = {}

		# ugly iterate through testsuite object
		for case in testcases:
			for i,test in enumerate(case):
				tcs[((test._tests)[0].__class__.__name__)] = tn
				for j in range(0,test.countTestCases()):
					 testnames["test-name"] = (case[i]._tests[j])._testMethodName
					 tn.append(testnames)
					 testnames = {}
				tn = []
		self.data["test-cases"] = tcs



	def addResultsJson(self, results, timestamp):
		'''
		This method should be used after the tests have been run. It adds the results to the existing self.data dictionary. 

		Args:
			results (unittest.runner.TextTestResult): This is the result object from running the unittest suite

		Returns:
			None

		Examples:
			Pass the result object from unittest as the only arguement. 
			This can be passed as a variable or dynamically causing the tests to run within the method call. Passing as a variable is recommended
			ex. 1:
				results = unittest.TextTestRunner().run(suite)
				PrettyUnit.addResultsJson(results)
			ex. 2:
				PrettyUnit.addResultsJson(unittest.TextTestRunner().run(suite))
		'''
		TOTAL_TEST_RUN = results.testsRun
		TOTAL_TEST_ERRORS = len(results.errors)
		TOTAL_TEST_FAILURES = len(results.failures)
		TOTAL_TEST_SKIPPED = len(results.skipped)
		self.data["timestamp"] = str(timestamp)
		self.data["tests-run"] = TOTAL_TEST_RUN
		self.data["tests-error"] = TOTAL_TEST_ERRORS
		self.data["tests-failure"] = TOTAL_TEST_FAILURES
		self.data["tests-skipped"] = TOTAL_TEST_SKIPPED
		# if there are errors, map them back to each test
		if TOTAL_TEST_ERRORS > 0:
			for i in range(TOTAL_TEST_ERRORS):
				for case in self.data["test-cases"]:
					for test in self.data["test-cases"][case]:
						if (results.errors[i][0]._testMethodName) == test["test-name"]:
							test["result"] = "error"
							test["message"] = results.errors[i][1]
		# if there are failures, map them back to each test
		if TOTAL_TEST_FAILURES > 0:
			for i in range(TOTAL_TEST_FAILURES):
				for case in self.data["test-cases"]:
					for test in self.data["test-cases"][case]:
						if (results.failures[i][0]._testMethodName) == test["test-name"]:
							test["result"] = "failure"
							test["message"] = results.failures[i][1]
		# if a test is skipped, label it
		if TOTAL_TEST_SKIPPED > 0:
			for i in range(TOTAL_TEST_SKIPPED):
				for case in self.data["test-cases"]:
					for test in self.data["test-cases"][case]:
						if (results.skipped[i][0]._testMethodName) == test["test-name"]:
							test["result"] = "skipped"
							test["message"] = results.skipped[i][1]
		# if there are no additional attributes for a test, we assume it has passed
		for i in range(TOTAL_TEST_RUN):
				for case in self.data["test-cases"]:
					for test in self.data["test-cases"][case]:
						if len(test) == 1:
							test["result"] = "passed"
							test["message"] = None



	def generateJson(self):
		'''
		Generates a json object using the information stored in the self.data dictionary.  
		This function should only be run after populateJson() and addResultsJson()

		Args:
			None

		Returns:
			json (str): This is a string generated by the json module, if this is run last it should be a valid json object that contains 
					    all executed unittest data
		'''
		return json.dumps(self.data)










