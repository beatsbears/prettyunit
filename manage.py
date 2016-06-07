#! /usr/bin/env python

from prettysite import app, db
from prettysite.models import Suite, TestCase, Test, Server
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)


@manager.command
def create_test_data():
    # create some test data
    db.session.add(Server(ServerName='test_server', ServerOS='linux'))
    db.session.add(Suite(SuiteName='test_suite', ServerId=1))
    db.session.add(TestCase(SuiteId=1, TestCaseName='test_case_1', TestCount=2, PassCount=1, SkipCount=1))
    db.session.add(TestCase(SuiteId=1, TestCaseName='test_case_2', TestCount=2, ErrorCount=1, FailCount=1))
    db.session.add(Test(TestCaseId=1, TestName='pass_test', Result='passed'))
    db.session.add(Test(TestCaseId=1, TestName='skip_test', Message='WIP', Result='skipped'))
    db.session.add(Test(TestCaseId=2, TestName='error_test', Message='Stacktrace: blahh', Result='error'))
    db.session.add(Test(TestCaseId=2, TestName='failed_test', Message='1 != 2', Result='failure'))
    db.session.commit()
    print 'Test data added to the database'

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()
