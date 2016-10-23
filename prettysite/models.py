from datetime import datetime
from prettysite import db
from sqlalchemy import desc
from collections import OrderedDict


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
    ProjectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, default=0)

    @staticmethod
    def results(id):
        res = Suite.query.filter(Suite.id == id).first()
        return [res.PassCount, res.FailCount, res.ErrorCount, res.SkipCount]

    @staticmethod
    def timeline(projectid):
        return Suite.query.with_entities(Suite.PassCount, Suite.FailCount, Suite.ErrorCount, Suite.SkipCount, Suite.DateRun).filter(Suite.ProjectId == projectid).order_by((Suite.DateRun)).all()

    @staticmethod
    def listsuites():
        objlist = Suite.query.with_entities(Suite.id, Suite.SuiteName, Suite.DateRun).order_by(desc(Suite.DateRun)).all()
        returndict = OrderedDict()
        for suite in objlist:
            returndict[suite.id] = [suite.SuiteName, suite.DateRun]
        return returndict

    @staticmethod
    def isdupe(name, date, server_id):
        return bool(Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date, Suite.ServerId == server_id).first() > 0)

    @staticmethod
    def getsuiteid(name, date):
        if Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date).first() > 0:
            return Suite.query.filter(Suite.SuiteName == name, Suite.DateRun == date).first().id
        else:
            return 0

    @staticmethod
    def does_exist(id):
        return bool(Suite.query.filter(Suite.id == id).first() > 0)

    @staticmethod
    def get_suites_by_project(projectid):
        objlist = Suite.query.with_entities(Suite.id, Suite.SuiteName, Suite.DateRun).filter(Suite.ProjectId == projectid).order_by(desc(Suite.DateRun)).all()
        returndict = OrderedDict()
        for suite in objlist:
            returndict[suite.id] = [suite.SuiteName, suite.DateRun]
        return returndict

    @staticmethod
    def get_suite_details(id):
        details = Suite.query.with_entities(Suite.PassCount, Suite.TestCount, Project.ProjectName, Server.ServerName, Server.ServerOS, Suite.DateRun).join(Project, Server).filter(Suite.id == id).all()
        time = details[0][5].strftime("%m/%d/%y %H:%M UTC")
        if details[0][1] > 0:
            passRate = float(details[0][0])/float(details[0][1])*100
        else:
            passRate = 0
        serverName = details[0][3]
        serverOS = details[0][4]
        projectname = details[0][2]
        return [passRate, time, projectname, serverName, serverOS]


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
    Time = db.Column(db.Float, nullable=False, default=0.0)
    tests = db.relationship('Test', backref='testcase', lazy='dynamic')

    @staticmethod
    def gettestcaseid(name, date):
        if TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first() > 0:
            return TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first().id
        else:
            return 0

    @staticmethod
    def isdupe(name, date):
        return bool(TestCase.query.filter(TestCase.TestCaseName == name, TestCase.DateRun == date).first() > 0)

    @staticmethod
    def get_testcase_by_suiteid(id):
        if TestCase.query.filter(TestCase.SuiteId == id).first() > 0:
            return TestCase.query.filter(TestCase.SuiteId == id).all()
        else:
            return 0


## --------------------------------- TEST ---------------------------------------------
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TestCaseId = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
    TestName = db.Column(db.String, nullable=False)
    Message = db.Column(db.String)
    Result = db.Column(db.String, nullable=False)

    @staticmethod
    def isdupe(name, caseid):
        return bool(Test.query.filter(Test.TestCaseId == caseid, Test.TestName == name).first() > 0)

    @staticmethod
    def total_test_count():
        passes = Test.query.filter(Test.Result == "passed").count()
        fails = Test.query.filter(Test.Result == "failed").count()
        errors = Test.query.filter(Test.Result == "error").count()
        skips = Test.query.filter(Test.Result == "skipped").count()
        return [passes, fails, errors, skips]

    @staticmethod
    def get_test_by_testcaseid(id):
        if Test.query.filter(Test.TestCaseId == id).first() > 0:
            return Test.query.filter(Test.TestCaseId == id).all()
        else:
            return 0

## --------------------------------- SERVER ---------------------------------------------
class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ServerName = db.Column(db.String, nullable=False)
    ServerOS = db.Column(db.String, nullable=False)
    DateAdded = db.Column(db.DateTime, default=datetime.utcnow())
    suites = db.relationship('Suite', backref='server', lazy='dynamic')

    @staticmethod
    def isdupe(name):
        return bool(Server.query.filter(Server.ServerName == name).first())

    @staticmethod
    def getserverid(name):
        if Server.query.filter(Server.ServerName == name).first() > 0:
            return Server.query.filter(Server.ServerName == name).first().id
        else:
            return 0

## --------------------------------- PROJECT ---------------------------------------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ProjectName = db.Column(db.String, nullable=False)
    ProjectDescription  = db.Column(db.String, nullable=False, default="Not set yet")
    ProjectLanguage = db.Column(db.String, nullable=False, default="Unknown")
    ProjectUrl = db.Column(db.String, nullable=False, default="Unknown")

    @staticmethod
    def getprojectid(name):
        if Project.query.filter(Project.ProjectName == name).first() > 0:
            return Project.query.filter(Project.ProjectName == name).first().id
        else:
            return 0

    @staticmethod
    def does_exist(id):
        return bool(Project.query.filter(Project.id == id).first() > 0)

    @staticmethod
    def listprojects():
        return Project.query.with_entities(Project.id, Project.ProjectName).order_by(Project.id).all()

    @staticmethod
    def isdupe(name):
        return bool(Project.query.filter(Project.ProjectName == name).first())

    @staticmethod
    def getprojectdescription(id):
        return Project.query.with_entities(Project.ProjectDescription).filter(Project.id == id).first()

    @staticmethod
    def getprojectlanguage(id):
        return Project.query.with_entities(Project.ProjectLanguage).filter(Project.id == id).first()

    @staticmethod
    def getprojecturl(id):
        return Project.query.with_entities(Project.ProjectUrl).filter(Project.id == id).first()

    @staticmethod
    def getprojectdetails(id):
        try:
            return Project.query.with_entities(Project.id, Project.ProjectName, Project.ProjectDescription, Project.ProjectLanguage, Project.ProjectUrl).filter(Project.id == id).all()
        except:
            return 0
    @staticmethod
    def setprojectfields(id, content_dict):
        try:
            val = Project.query.filter(Project.id == id).first()
            for key, value in content_dict.items():
                if key == "Project":
                    val.ProjectName = value
                elif key == "Description":
                    val.ProjectDescription = value
                elif key == "Language":
                    val.ProjectLanguage = value
                elif key == "Url":
                    val.ProjectUrl = value
            db.session.commit()
            return True
        except:
            return False


## ---------------------------- SETTINGS -------------------------------------------------
class PrettySiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Value = db.Column(db.String, nullable=False)
    Type = db.Column(db.String, nullable=False)
    Locked = db.Column(db.Boolean, nullable=False, default=True)

    @staticmethod
    def getsettingvalue(name):
        if PrettySiteSettings.query.filter(PrettySiteSettings.Name == name).first() > 0:
            return PrettySiteSettings.query.filter(PrettySiteSettings.Name == name).first().Value
        else:
            return 0

    @staticmethod
    def setsettingvalue(name, value):
        if PrettySiteSettings.query.filter(PrettySiteSettings.Name == name).first() > 0:
            try:
                val = PrettySiteSettings.query.filter(PrettySiteSettings.Name == name).first()
                val.Value = value
                db.session.commit()
                return True
            except:
                return False
        else:
            db.session.add(PrettySiteSettings(Name=name, Value=value, Type="String", Locked=False))
            db.session.commit()

    @staticmethod
    def listsettings():
        return PrettySiteSettings.query.with_entities(PrettySiteSettings.Name, PrettySiteSettings.Value, PrettySiteSettings.Type, PrettySiteSettings.Locked).order_by(PrettySiteSettings.id).all()



## ---------------------------- Token -------------------------------------------------
class APIToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Token = db.Column(db.String, nullable=False)

    @staticmethod
    def getAPItoken():
        return APIToken.query.with_entities(APIToken.Token).first()

    @staticmethod
    def replaceAPItoken(new_token):
        print "Hit"
        try:
            if APIToken.query.filter(APIToken.id == 1).first() < 1:
                print "Hit2"
                db.session.add(APIToken(Token=new_token))
                db.session.commit()
            else:
                print "Hit3"
                val = APIToken.query.filter(APIToken.id == 1).first()
                val.token == new_token
                db.session.commit()
            return True
        except:
            print "Hit4"
            return False

    @staticmethod
    def validateToken(test_token):
       if test_token == str(APIToken.query.with_entities(APIToken.Token).first()[0]):
           return True
       return False