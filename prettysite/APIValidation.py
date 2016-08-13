
from dateutil.parser import parse
from prettysite import db
from models import Suite, TestCase, Test, Server, Project

class APIHandler():

    def testcase_parser(self, name, data, date, suite):
        caseName = name
        dateRun = date
        suiteId = Suite.getsuiteid(suite, dateRun)
        testResults = [0, 0, 0, 0]  # pass, fail, error, skip
        for test in data:
            if self.is_result_valid(test["result"]):
                if test["result"] == "passed":
                    testResults[0] += 1
                elif test["result"] == "failure":
                    testResults[1] += 1
                elif test["result"] == "error":
                    testResults[2] += 1
                else:
                    testResults[3] += 1
        testPass, testFail, testError, testSkip = testResults
        testCount = sum(testResults)
        if not TestCase.isdupe(caseName, dateRun):
            db.session.add(TestCase(SuiteId=suiteId, TestCaseName=caseName, TestCount=testCount,
                                    PassCount=testPass, FailCount= testFail, ErrorCount=testError,
                                    SkipCount=testSkip, DateRun=dateRun))
            db.session.commit()
        else:
            pass

    def server_parser(self, json):
        serverName, osSystem = json["server"], json["system"]
        if serverName and osSystem:
            if not Server.isdupe(serverName):
                db.session.add(Server(ServerName=serverName, ServerOS=osSystem))
                db.session.commit()
            else:
                pass

    def tests_parser(self, json):
        testData = json['test-cases']
        dateRun = parse(json['timestamp'])
        suite = json['suite-name']
        print suite
        for testcase, data in testData.items():
            self.testcase_parser(testcase, data, dateRun, suite)
            testCaseId = TestCase.gettestcaseid(testcase, dateRun)
            for test in data:
                testName = test["test-name"]
                testMessage = test["message"]
                testResult = test["result"]
                if not Test.isdupe(testName, testCaseId):
                    db.session.add(Test(TestCaseId=testCaseId, TestName=testName, Message=testMessage, Result=testResult))
                    db.session.commit()
                else:
                    pass

    def suite_parser(self, json):
        suiteName = json['suite-name']
        dateRun = parse(json['timestamp'])
        testType = 'unittest'
        testCount = self.assign_or_default(json['test-to-run'],0)
        testFail = self.assign_or_default(json['tests-failure'],0)
        testError = self.assign_or_default(json['tests-error'],0)
        testSkip = self.assign_or_default(json['tests-skipped'],0)
        testRun = self.assign_or_default(json['tests-run'],0)
        testPass = (testRun - (testError + testSkip + testFail)) \
                    if (testRun - (testError + testSkip + testFail)) >= 0 \
                    else 0 # pass = #tests run - all other results
        serverId = Server.getserverid(json['server'])
        projectId = Project.getprojectid(json['project'])
        if not Suite.isdupe(suiteName, dateRun, serverId):
            db.session.add(Suite(SuiteName=suiteName, TestType=testType, TestCount=testCount,
                             PassCount=testPass , FailCount=testFail, ErrorCount=testError,
                             SkipCount=testSkip, DateRun=dateRun, ServerId=serverId, ProjectId=projectId))
            db.session.commit()
        else:
            pass

    def project_parser(self, json):
        projectName = json["project"]
        if not Project.isdupe(projectName):
            db.session.add(Project(ProjectName=projectName))
            db.session.commit()
        else:
            pass


## ---------------------------------- Helper Methods --------------------------------------------

    def is_result_valid(self, result):
        validString = ("passed", "failure", "skipped", "error")
        if result.lower() in validString:
            return True
        return False

    def assign_or_default(self,value,default):
        if value != None:
            return value
        else:
            return default
