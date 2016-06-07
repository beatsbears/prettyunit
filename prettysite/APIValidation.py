
from dateutil.parser import parse
from prettysite import db
from models import Suite, TestCase, Test, Server

class api_handler():

    def testcase_parser(self, name, data, date, suite):
        case_name = name
        date_run = date
        suite_id = Suite.getsuiteid(suite, date_run)
        test_results = [0, 0, 0, 0]  # pass, fail, error, skip
        for test in data:
            if self.is_result_valid(test["result"]):
                if test["result"] == "passed":
                    test_results[0] += 1
                elif test["result"] == "failure":
                    test_results[1] += 1
                elif test["result"] == "error":
                    test_results[2] += 1
                else:
                    test_results[3] += 1
        test_pass, test_fail, test_error, test_skip = test_results
        test_count = sum(test_results)
        if not TestCase.isdupe(case_name, date_run):
            db.session.add(TestCase(SuiteId=suite_id, TestCaseName=case_name, TestCount=test_count,
                                    PassCount=test_pass, FailCount= test_fail, ErrorCount=test_error,
                                    SkipCount=test_skip, DateRun=date_run))
            db.session.commit()
        else:
            pass

    def server_parser(self, json):
        server_name, os_system = json["server"], json["system"]
        if server_name and os_system:
            if not Server.isdupe(server_name):
                db.session.add(Server(ServerName=server_name, ServerOS=os_system))
                db.session.commit()
            else:
                pass

    def tests_parser(self, json):
        testdata = json['test-cases']
        date_run = parse(json['timestamp'])
        suite = json['suite-name']
        print suite
        for testcase, data in testdata.items():
            self.testcase_parser(testcase, data, date_run, suite)
            testCaseId = TestCase.gettestcaseid(testcase, date_run)
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
        suite_name = json['suite-name']
        date_run = parse(json['timestamp'])
        test_type = 'unittest'
        test_count = self.assign_or_default(json['test-to-run'],0)
        test_fail = self.assign_or_default(json['tests-failure'],0)
        test_error = self.assign_or_default(json['tests-error'],0)
        test_skip = self.assign_or_default(json['tests-skipped'],0)
        test_run = self.assign_or_default(json['tests-run'],0)
        test_pass = (test_run - (test_error + test_skip + test_fail)) \
                    if (test_run - (test_error + test_skip + test_fail)) >= 0 \
                    else 0 # pass = #tests run - all other results
        server_id = Server.getserverid(json['server'])
        if not Suite.isdupe(suite_name, date_run, server_id):
            db.session.add(Suite(SuiteName=suite_name, TestType=test_type, TestCount=test_count,
                             PassCount=test_pass , FailCount=test_fail, ErrorCount=test_error,
                             SkipCount=test_skip, DateRun=date_run, ServerId=server_id))
            db.session.commit()
        else:
            pass
## ---------------------------------- Helper Methods --------------------------------------------

    def is_result_valid(self, result):
        valid_str = ("passed", "failure", "skipped", "error")
        if result.lower() in valid_str:
            return True
        return False

    def assign_or_default(self,value,default):
        if value != None:
            return value
        else:
            return default
