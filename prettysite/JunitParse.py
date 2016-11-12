'''
prettyunit json parsing & helper methods
ascott 10/2016
'''
import xml.etree.ElementTree as ET
from datetime import datetime

class JunitParse():

	def testcase_parse(self, suite):
		testcases = []
		for testcase in suite.findall('testcase'):
			testcase_dict = {}
			if testcase.find('error') != None:
				testcase_dict['result'] = 'error'
				if 'message' in testcase.find('error').attrib:
					testcase_dict['message'] = "{} : {}".format(testcase.find('error').attrib['message'],testcase.find('error').text)
				else:
					testcase_dictb['message'] = "{}".format(testcase.find('error').text)
			elif testcase.find('failure') != None:
				testcase_dict['result'] = 'failure'
				if 'message' in testcase.find('failure').attrib:
					testcase_dict['message'] = "{} : {}".format(testcase.find('failure').attrib['message'],testcase.find('failure').text)
				else:
					testcase_dict['message'] = "{}".format(testcase.find('failure').text)
			elif testcase.find('skipped') != None:
				testcase_dict['result'] = 'skipped'
				if 'skipped' in testcase.find('skipped').attrib:
					testcase_dict['message'] = "{} : {}".format(testcase.find('skipped').attrib['message'],testcase.find('skipped').text)
				else:
					testcase_dict['message'] = "{}".format(testcase.find('skipped').text)
			else:
				testcase_dict["result"] = "passed"
				testcase_dict['message'] = 'None'

			if "name" in testcase.attrib:
				testcase_dict["test-name"] = testcase.attrib["name"]
			if "time" in testcase.attrib:
				testcase_dict["time"] = float(testcase.attrib["time"])
			else:
				testcase_dict["time"] = 0.0

			testcases.append(testcase_dict)
		return testcases

	def suitedetail_parse(self, suite):
		suite_details = {}
		if "tests" in suite.attrib:
			suite_details["tests-run"] = int(suite.attrib["tests"])
			suite_details["test-to-run"] = int(suite.attrib["tests"])
		else:
			suite_details["tests-run"] = 0
			suite_details["test-to-run"] = 0

		if "skipped" in suite.attrib:
			suite_details["tests-skipped"] = int(suite.attrib["skipped"])
		else:
			suite_details["tests-skipped"] = 0

		if "failures" in suite.attrib:
			suite_details["tests-failure"] = int(suite.attrib["failures"])
		else:
			suite_details["tests-failure"] = 0

		if "errors" in suite.attrib:
			suite_details["tests-error"] = int(suite.attrib["errors"])
		else:
			suite_details["tests-error"] = 0

		if "timestamp" in suite.attrib:
			suite_details["timestamp"] = suite.attrib["timestamp"]
		else:
			suite_details["timestamp"] = str(datetime.utcnow())

		if "name" in suite.attrib:
			suite_details["suite-name"] = suite.attrib["name"]
		return suite_details

	def junit_parse(self, xml):
		tree = ET.ElementTree(ET.fromstring(xml))
		root = tree.getroot()
		json = []

		for suite in root.findall('testsuite'):
			suite_details = self.suitedetail_parse(suite)
			testcases = self.testcase_parse(suite)
			suite_details["test-cases"] = {"Default": testcases}
			json.append(suite_details)

		return json

	def add_project(self, json, project='None', system='Unknown', server='Unknown'):
		for i in range(len(json)):
			json[i]["project"] = project
			json[i]["system"] = system
			json[i]["server"] = server
			json[i]["puv"] = "1.0"
		return json