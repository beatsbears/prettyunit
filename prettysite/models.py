from datetime import datetime
from prettysite import db



## --------------------------------- SUITE ---------------------------------------------
class Suite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SuiteName = db.Column(db.Text, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow())
    TestType = db.Column(db.Text, nullable=False, default='python unittest')
    TestCount = db.Column(db.Integer,nullable=False, default=0)
    PassCount = db.Column(db.Integer,nullable=False, default=0)
    FailCount = db.Column(db.Integer,nullable=False, default=0)
    ErrorCount = db.Column(db.Integer,nullable=False, default=0)
    SkipCount = db.Column(db.Integer,nullable=False, default=0)
    DateRun = db.Column(db.DateTime, default=datetime.utcnow())
    ServerId = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    testcases = db.relationship('TestCase', backref='suite', lazy='dynamic')

    @staticmethod
    def results(id):
        res = Suite.query.filter(Suite.id == id)
        return [res.PassCount, res.FailCount, res.ErrorCount, res.SkipCount]

    @staticmethod
    def isdupe(name, date, server_id):
        if Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date, Suite.ServerId == server_id).first() > 0:
            return True
        return False

    @staticmethod
    def getsuiteid(name, date):
        if Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date).first() > 0:
            return Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date).first().id
        else:
            return 0



## --------------------------------- TESTCASE ---------------------------------------------
class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SuiteId = db.Column(db.Integer, db.ForeignKey('suite.id'), nullable=False)
    TestCaseName = db.Column(db.Text, nullable=False)
    TestCount = db.Column(db.Integer,nullable=False, default=0)
    PassCount = db.Column(db.Integer,nullable=False, default=0)
    FailCount = db.Column(db.Integer,nullable=False, default=0)
    ErrorCount = db.Column(db.Integer,nullable=False, default=0)
    SkipCount = db.Column(db.Integer,nullable=False, default=0)
    DateRun = db.Column(db.DateTime, default=datetime.utcnow())
    tests = db.relationship('Test', backref='testcase', lazy='dynamic')

    @staticmethod
    def gettestcaseid(name, date):
        if TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first() > 0:
            return TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first().id
        else:
            return 0

    @staticmethod
    def isdupe(name, date):
        if TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first() > 0:
            return True
        return False


## --------------------------------- TEST ---------------------------------------------
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TestCaseId = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
    TestName = db.Column(db.String, nullable=False)
    Message = db.Column(db.String)
    Result = db.Column(db.String, nullable=False)

    @staticmethod
    def isdupe(name, caseid):
        if Test.query.filter(Test.TestCaseId == caseid, Test.TestName == name).first() > 0:
            return True
        return False


## --------------------------------- SERVER ---------------------------------------------
class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ServerName = db.Column(db.String, nullable=False)
    ServerOS = db.Column(db.String, nullable=False)
    DateAdded = db.Column(db.DateTime, default=datetime.utcnow())
    suites = db.relationship('Suite', backref='server', lazy='dynamic')

    @staticmethod
    def isdupe(name):
        if Server.query.filter(Server.ServerName == name).first():
            return True
        return False

    @staticmethod
    def getserverid(name):
        if Server.query.filter(Server.ServerName == name).first() > 0:
            return Server.query.filter(Server.ServerName == name).first().id
        else:
            return 0
