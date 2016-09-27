from flask import Flask, render_template, request, url_for

from prettysite import app, db
from models import Suite, TestCase, Test, Server, Project, PrettySiteSettings
from APIValidation import APIHandler

# ----------------------------------------------------------------------------------------
@app.route('/')
def index():
    projects = Project.listprojects()
    settings = PrettySiteSettings.listsettings()
    name = PrettySiteSettings.getsettingvalue("Name")
    print settings
    return render_template('project.html', name=name, projects=projects, settings=settings)



@app.route('/<int:projectid>')
def project_overview(projectid):
    tl = Suite.timeline(projectid)
    settings = PrettySiteSettings.listsettings()
    print tl
    timeline = [[],[],[],[]] # skip, error, fail, pass
    dates = []
    for t in tl:
        timeline[0].append(t[3])
        timeline[1].append(t[2])
        timeline[2].append(t[1])
        timeline[3].append(t[0])
        dates.append(t[4].strftime("%m/%d/%y %H:%M UTC"))
    suitelist =  [item for item in Suite.get_suites_by_project(projectid).items()]
    return render_template('index.html', timeline=timeline, timeline_dates=dates, suitelist=suitelist, settings=settings)


@app.route('/<int:projectid>/<int:suiteid>')
def suite_overview(suiteid, projectid):

    tl = Suite.timeline(projectid)
    settings = PrettySiteSettings.listsettings()
    timeline = [[],[],[],[]] # skip, error, fail, pass
    dates = []
    for t in tl:
        timeline[0].append(t[3])
        timeline[1].append(t[2])
        timeline[2].append(t[1])
        timeline[3].append(t[0])
        dates.append(t[4].strftime("%m/%d/%y %H:%M UTC"))

    suiteDetails = []
    details = Suite.get_suite_details(suiteid)
    suiteDetails.append(["Pass Rate", str(details[0])])
    suiteDetails.append(["Last Run", str(details[1])])
    suiteDetails.append(["Project Name", str(details[2])])
    suiteDetails.append(["Server", str(details[3])])
    suiteDetails.append(["Platform", str(details[4])])

    if Suite.does_exist(suiteid):
        suiteResults = Suite.results(suiteid)
        caseList = [[case.id, case.TestCaseName, case.DateRun]
                    for case in TestCase.get_testcase_by_suiteid(suiteid)]
        caseResults = [[case.PassCount, case.FailCount, case.ErrorCount, case.SkipCount]
                        for case in TestCase.get_testcase_by_suiteid(suiteid)]

        testResults = []
        for i, case in enumerate(caseList):
            testResults.append([])
            for test in Test.get_test_by_testcaseid(case[0]):
                testResults[i].append([test.TestName, test.Message, test.Result])

        caseToDisplay = (0 if request.args.get('case') is None else int(request.args.get('case')))
        if caseToDisplay != 0:
            for i, c in enumerate(caseList):
                if c[0] == int(caseToDisplay):
                    caseToDisplay = i

        return render_template('suite.html', timeline=timeline, timeline_dates=dates,
                               suite_results=suiteResults, testcaseslist=caseList,
                               suiteid=suiteid, caseresults=caseResults,
                               testresults=testResults, casetodisplay=caseToDisplay, suitedetails=suiteDetails,
                               settings=settings)
    else:
        return '', 404





@app.route('/settings')
def settings():
    return '', 200


@app.route('/settings', methods=['POST'])
def update_settings():
    try:
        content = request.get_json(silent=True)
        for key, val in content.items():
            if val[1]:
                PrettySiteSettings.setsettingvalue(key,val[0])
        return '', 200
    except:
        return '', 500



# -------------------------------- API ----------------------------------------------------
@app.route('/version', methods=['GET', 'HEAD'])
def version():
    return (app.config['VERSION'], 200)

@app.route('/api/results', methods=['POST'])
def add_results():
    APIV = APIHandler()
    content = request.get_json(silent=True)
    # Parse Project
    APIV.project_parser(content)
    # Parse Server
    APIV.server_parser(content)
    # Parse Suite
    APIV.suite_parser(content)
    # Parse TestCases and Tests
    APIV.tests_parser(content)
    return ('', 200)


