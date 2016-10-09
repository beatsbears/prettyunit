from flask import Flask, render_template, request, url_for

from prettysite import app, db
from models import Suite, TestCase, Test, Server, Project, PrettySiteSettings, APIToken
from APIValidation import APIHandler
from APIKey import APIKey

import json

if app.config['DEBUG'] == True:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


# ----------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    projects = Project.listprojects()
    settings = PrettySiteSettings.listsettings()
    name = PrettySiteSettings.getsettingvalue("Name")
    return render_template('project.html', name=name, projects=projects, settings=settings)

@app.route('/<int:projectid>', methods=['GET'])
def project_overview(projectid):
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
    suitelist =  [item for item in Suite.get_suites_by_project(projectid).items()]
    name = PrettySiteSettings.getsettingvalue("Name")
    return render_template('index.html', timeline=timeline, name=name, timeline_dates=dates, suitelist=suitelist, settings=settings)


@app.route('/<int:projectid>/<int:suiteid>', methods=['GET'])
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

        name = PrettySiteSettings.getsettingvalue("Name")

        return render_template('suite.html', timeline=timeline, name=name, timeline_dates=dates,
                               suite_results=suiteResults, testcaseslist=caseList,
                               suiteid=suiteid, caseresults=caseResults,
                               testresults=testResults, casetodisplay=caseToDisplay, suitedetails=suiteDetails,
                               settings=settings)
    else:
        return '', 404






# -------------------------------- API ----------------------------------------------------
@app.route('/version', methods=['GET', 'HEAD'])
def version():
    return (app.config['VERSION'], 200)

@app.route('/settings', methods=['GET', 'HEAD'])
def settings():
    return '', 200

@app.route('/settings', methods=['POST'])
def update_settings():
    try:
        content = request.get_json(silent=True)
        print content
        newKeys = {}
        for key, val in content.items():
            if val[1]:
                PrettySiteSettings.setsettingvalue(key,val[0])
            if key == "Key1" or key == "Key2":
                newKeys[key] = val[0]
        keyHandler = APIKey()
        APIToken.replaceAPItoken(keyHandler.createMasterKey(newKeys["Key1"], newKeys["Key2"]))
        return '', 200
    except:
        return '', 500

@app.route('/api/results', methods=['POST'])
def add_results():
    keygen = APIKey()
    useTokens = keygen.areTokensEnabledAndExist()
    if useTokens:
        keyHeader = request.headers.get('X-Keys')
        keys = json.loads(keyHeader)
        token = keygen.createMasterKey(keys["Key1"], keys["Key2"])
        if APIToken.validateToken(token):
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
        else:
            return ('Invalid token', 401)
    else:
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

@app.route('/token', methods=['GET'])
def genetate_tokens():
    keygen = APIKey()
    k1 = keygen.generateKey()
    k2 = keygen.generateKey()
    data = {"Key1" : k1, "Key2" : k2}
    return (str(json.dumps(data)), 200)

@app.route('/usetokens', methods=['GET'])
def usertokens():
    keygen = APIKey()
    keygen.areTokensEnabledAndExist()
    return ('',200)