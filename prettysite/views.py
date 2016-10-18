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
    try:
        projects = Project.listprojects()
        settings = PrettySiteSettings.listsettings()
        name = PrettySiteSettings.getsettingvalue("Name")
        return render_template('project.html', name=name, projects=projects, settings=settings)
    except:
        return ('', 500)

@app.route('/<int:projectid>', methods=['GET'])
def project_overview(projectid):
    try:
        tl = Suite.timeline(projectid)
        settings = PrettySiteSettings.listsettings()
        project = Project.getprojectdetails(projectid)[0]
        project_desc = {'id' : project[0], 'name' : project[1], 'description' : project[2], 'language' : project[3], 'url' : project[4]}
        print project_desc
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
        return render_template('index.html', timeline=timeline, name=name, timeline_dates=dates, suitelist=suitelist, settings=settings, project_desc=project_desc)
    except:
        return ('', 500)




@app.route('/<int:projectid>/<int:suiteid>', methods=['GET'])
def suite_overview(suiteid, projectid):
    try:
        tl = Suite.timeline(projectid)
        settings = PrettySiteSettings.listsettings()
        project = Project.getprojectdetails(projectid)[0]
        project_desc = {'id' : project[0], 'name' : project[1], 'description' : project[2], 'language' : project[3], 'url' : project[4]}
        print project_desc
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
                                   settings=settings, project_desc=project_desc)
        else:
            return '', 404
    except:
        return ('', 500)





# -------------------------------- API ----------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

# -------------------------------- Version ------------------------------------------------
@app.route('/version', methods=['GET', 'HEAD'])
def version():
    '''
    Returns the current version of prettysite
    :return: 200 response if Version is set
             500 if there is an issue
    '''
    try:
        return (app.config['VERSION'], 200)
    except:
        return ('', 500)



# -------------------------------- Settings ------------------------------------------------
@app.route('/settings', methods=['GET', 'HEAD'])
def settings():
    '''
    This call can be used to return a json object containing the prettyunit settings.
    :return: 200 if successful
             500 if there was an error
    '''
    try:
        settings = PrettySiteSettings.listsettings()
        data = {'version' : settings[0][1], 'name' : settings[1][1], 'api_tokens_enabled' : settings[2][1]}
        if data['api_tokens_enabled'] == 'True':
            if settings[3][0] == 'Key2':
                data['Key2'] = settings[3][1]
            if settings[3][0] == 'Key1':
                data['Key1'] = settings[3][1]
            if settings[4][0] == 'Key2':
                data['Key2'] = settings[4][1]
            if settings[4][0] == 'Key1':
                data['Key1'] = settings[4][1]
        return (str(json.dumps(data)), 200)
    except:
        return ('', 500)

@app.route('/settings', methods=['POST'])
def update_settings():
    '''
    This call can be used to update the prettyunit settings. The second value in the tuple should always be "False" in order for this call to work.
    {
        "Name":[[str], "False"],
        "API Tokens Enabled":[["True" or "False"], "False"]
    }
    :return: 200 if successful
             500 if there was an error
    '''
    try:
        content = request.get_json(silent=True)
        print content
        newKeys = {}
        for key, val in content.items():
            if val[1] == "False":
                PrettySiteSettings.setsettingvalue(key,val[0])
            if key == "Key1" or key == "Key2":
                newKeys[key] = val[0]
        keyHandler = APIKey()
        APIToken.replaceAPItoken(keyHandler.createMasterKey(newKeys["Key1"], newKeys["Key2"]))
        return '', 200
    except:
        return '', 500



# -------------------------------- Results ------------------------------------------------
@app.route('/api/results', methods=['POST'])
def add_results():
    '''

    :return:
    '''
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





# -------------------------------- Security ------------------------------------------------
@app.route('/token', methods=['GET'])
def generate_tokens():
    '''
    This call should be used to get a new pair of API keys, which are combined to consititute a security token.
    :return: 200 and a json obj with the new key values
             500 if there was an error
    '''
    try:
        keygen = APIKey()
        k1 = keygen.generateKey()
        k2 = keygen.generateKey()
        data = {"Key1" : k1, "Key2" : k2}
        return (str(json.dumps(data)), 200)
    except:
        return ('', 500)

@app.route('/usetokens', methods=['GET'])
def usertokens():
    '''
    Can be used to check whether API tokens are enabled and populated
    :return: 200 for tokens ready for use
             404 if tokens are not enabled or populated
             500 if there was an error
    '''
    try:
        keygen = APIKey()
        if keygen.areTokensEnabledAndExist():
            return ('', 200)
        else:
            return ('', 404)
    except:
        return ('', 500)




# -------------------------------- Project ------------------------------------------------
@app.route('/project/<int:projectid>', methods=['PUT'])
def update_project(projectid):
    '''
    This call can be used to update the details of an existing project.
    {
        'Project': [str],
        'Url': [str],
        'Description': [str],
        'Language': [str]
    }
    :param projectid: Int - This should be the ID of an existing project.
    :return: 200 if successful
             404 if the project does not exist
             500 if there was an error
    '''
    if Project.does_exist(projectid):
        try:
            content = request.get_json(silent=True)
            Project.setprojectfields(projectid, content)
            return ('', 200)
        except:
            return ('', 500)
    return ('', 404)

@app.route('/project/<int:projectid>', methods=['GET'])
def get_project(projectid):
    '''
    This call should return a json object with the details for an existing project.
    :param projectid: Int - This should be the ID of an existing project.
    :return: 200 if successful
             404 if the project does not exist
             500 if there was an error
    '''
    if Project.does_exist(projectid):
        try:
            project = Project.getprojectdetails(projectid)[0]
            data = {'id' : project[0], 'name' : project[1], 'description' : project[2], 'language' : project[3], 'url' : project[4]}
            return (str(json.dumps(data)), 200)
        except:
            return ('', 500)
    return ('', 404)

@app.route('/project', methods=['GET'])
def list_projects():
    '''
    This call should return a list of all projects as an [id, project_name] list.
    :return: 200 List of project id/name pairs
             500 if error
    '''
    try:
        projects = Project.listprojects()
        return (str(json.dumps(projects)), 200)
    except:
        return ('', 500)