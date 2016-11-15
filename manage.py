#! /usr/bin/env python

from prettysite import app, db, APIKey
from prettysite.models import Suite, TestCase, Test, Server, Project, PrettySiteSettings, APIToken
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
import logging

manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)


@manager.command
def create_test_data():
    "Initializes the database with a test project"
    db.session.add(Project(ProjectName="Init"))
    db.session.add(Server(ServerName='test_server', ServerOS='linux'))
    db.session.add(Suite(SuiteName='test_suite', ServerId=1, ProjectId=1, TestCount=4, PassCount=1, SkipCount=1, FailCount=1, ErrorCount=1))
    db.session.add(TestCase(SuiteId=1, TestCaseName='test_case_1', TestCount=2, PassCount=1, SkipCount=1))
    db.session.add(TestCase(SuiteId=1, TestCaseName='test_case_2', TestCount=2, ErrorCount=1, FailCount=1))
    db.session.add(Test(TestCaseId=1, TestName='pass_test', Result='passed'))
    db.session.add(Test(TestCaseId=1, TestName='skip_test', Message='WIP', Result='skipped'))
    db.session.add(Test(TestCaseId=2, TestName='error_test', Message='Stacktrace: blahh', Result='error'))
    db.session.add(Test(TestCaseId=2, TestName='failed_test', Message='1 != 2', Result='failure'))
    db.session.commit()
    print('[+] Test data added to the database')

@manager.command
def set_default_settings():
    "Sets up the default settings"
    db.session.add(PrettySiteSettings(Name="Version",Value="0.1-ALPHA", Type="String"))
    db.session.add(PrettySiteSettings(Name="Name",Value=" prettyunit.", Type="String", Locked=False))
    db.session.add(PrettySiteSettings(Name="API Tokens Enabled",Value="False", Type="Bool", Locked=False))
    db.session.commit()
    print('[+] Default settings added successfully')

@manager.command
def dropdb():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print('[+] Dropped the database')

@manager.command
def _dropdb_script():
    "Drops database tables - no prompts"
    db.drop_all()

if __name__ == '__main__':
    manager.run()
