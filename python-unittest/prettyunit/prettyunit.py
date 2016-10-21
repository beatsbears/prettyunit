'''
python 2.7 unittest prettyunit wrapper

author: Andrew Scott
repo: https://github.com/beatsbears/prettyunit
'''
import unittest
import datetime
import json
import sys
import os
import socket
import requests

# pylint: disable=protected-access, line-too-long, invalid-name


class PrettyUnit(object):
    '''
    A framework to provide usable results for reporting from unittest.

    Attributes:
        data (dict): A dictionary storing all test that that will eventually be converted into a json str
        MACHINE_NAME (str): The name of the machine that the tests are running on
        SYSTEM (str): The OS platform name where the tests are running
        ...
    '''

    def __init__(self, projectName, API_key1=None, API_key2=None):
        '''
        Args:
            projectName (str): Name of the project, this is the top level separator for test data.
        '''
        self.data = {}
        self.PROJECT_NAME = projectName
        self.seed_data()
        self.PU_FORMAT_VERSION = '1.0'
        self.API_KEY1 = API_key1
        self.API_KEY2 = API_key2
        self.TOTAL_TEST_COUNT = 0

    def seed_data(self):
        '''
        This method is used to gather any non-test-specific information.

        Note: This method may be expanded in the future to allow for passing additional attributes to the PrettyUnit instance.
              However, for now it will only fetch and store the name of the machine the tests are running on.
        '''
        try:
            self.SYSTEM = sys.platform
            self.MACHINE_NAME = socket.gethostname()

        except IOError, error:
            print str(error)

    def generate_suite(self, suitename, *testcases):
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
            return suitename, test_suite
        except AttributeError, error:
            print '[!] Test suite generation failed! \n{}'.format(str(error))

    def populate_json(self, testsuite_name, *testcases):
        '''
        Initial json seeding and base creation prior to the results object

        Args:
            testsuite_name (str): This is the name returned by the suite method
            *testcases (list): This will be supplied by the suite._tests property. It is a list containing all tests
                               included in the suite.
        Returns:
            None
        '''
        # populate known value
        self.data["suite-name"] = testsuite_name
        self.data["server"] = self.MACHINE_NAME
        self.data["system"] = self.SYSTEM
        self.data["test-to-run"] = self.TOTAL_TEST_COUNT
        self.data["project"] = self.PROJECT_NAME
        self.data["puv"] = self.PU_FORMAT_VERSION


        tcs = {}
        tn = []
        testnames = {}

        # ugly iterate through testsuite object
        for case in testcases:
            for i, test in enumerate(case):
                tcs[(test._tests[0].__class__.__name__)] = tn
                for j in range(0, test.countTestCases()):
                    testnames["test-name"] = (case[i]._tests[j])._testMethodName
                    tn.append(testnames)
                    testnames = {}
                tn = []
        self.data["test-cases"] = tcs

    def add_results_json(self, results):
        # pylint: disable=too-many-branches
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
        self.data["timestamp"] = str(datetime.datetime.utcnow())
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

    def validate_directory(self, direct):
        '''
        Validate that directory exists and is writeable.

        Args:
            dir (str): Target directory on local filesystem.

        Returns:
            Bool: True is returned if the directory exists and can be written to.
        '''
        if not os.path.isdir(direct):
            return False

        return bool(os.access(direct, os.W_OK))

    def generate_json(self):
        '''
        Generates a json object using the information stored in the self.data dictionary.
        This function should only be run after populateJson() and addResultsJson()

        Args:
            None

        Returns:
            json (str): This is a string generated by the json module, if this is run last it should be a valid json object that contains
                        all executed unittest data.
        '''
        return json.dumps(self.data)

    def generate_json_and_save(self, path):
        '''
        Saves the json dump file locally in the specified path.

        Args:
            path (str): The directory location to save the json result file.

        Returns:
            None

        Note:
            The file name format is {suite-name}_{unix-timestamp}.json
        '''
        resultname = self.data['suite-name'] + '_' + str(datetime.datetime.utcnow().strftime("%s")) + '.json'
        if self.validate_directory(path):
            with open(path + resultname, 'w') as f:
                f.write(json.dumps(self.data))
        else:
            raise IOError('Directory: {} could not be accessed.'.format(path))

    def generate_json_and_send_http(self, host):
        '''
        This method sends the json results as the body of an HTTP POST requests to your prettyunit server.

        Args:
            host (str): URL of API endpoint

        Returns:
            Bool: True is returned is the server responds with a 200 OK
        '''
        if self.API_KEY1 != None and self.API_KEY2 != None:
            key_string = '"Key1":{}, "Key2":{}'.format(self.API_KEY1, self.API_KEY2)
            headers = {'content-type': 'application/json',
                        'X-Keys': key_string
                       }
        else:
            headers = {'content-type': 'application/json'
                       }
        url = host
        r = requests.post(url, data=json.dumps(self.data), headers=headers)
        return bool(r.status_code == 200)







