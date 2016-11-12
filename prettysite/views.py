"""prettyunit - prettysite views.py
Andrew Scott 10/21/2016"""

#pylint: disable=line-too-long, invalid-name, bare-except, broad-except
import json

from flask import render_template, request
from prettysite import app
from prettysite.models import Suite, TestCase, Test, Project, PrettySiteSettings, APIToken
from prettysite.APIValidation import APIHandler
from prettysite.APIKey import APIKey





if app.config['DEBUG']:
    import logging
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.DEBUG)


# ----------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    '''
    This should return the base page, typically where the user would pick which project they'd
    like to work in.
    :return: 200 if successful
             500 if an error occurs
    '''
    try:
        projects = Project.listprojects()
        site_settings = PrettySiteSettings.listsettings()
        name = PrettySiteSettings.getsettingvalue("Name")
        return render_template('project.html', name=name, projects=projects, settings=site_settings)
    except Exception, err:
        print err
        return ('', 500)

@app.route('/<int:projectid>', methods=['GET'])
def project_overview(projectid):
    '''
    This route should return the base page of a project, displaying aggregated results of all test suites.
    :param projectid: int - This should be the ID of an existing project.
    :return: 200 returns html page template and a variety of params to the template.
             500 if an error occurs
    '''
    try:
        dates, timeline, site_settings, project_desc = details_from_project_id(projectid)
        suitelist = [item for item in Suite.get_suites_by_project(projectid).items()]
        name = PrettySiteSettings.getsettingvalue("Name")
        return render_template('index.html', timeline=timeline, name=name, timeline_dates=dates, suitelist=suitelist, settings=site_settings, project_desc=project_desc)
    except Exception, err:
        print err
        return ('', 500)




@app.route('/<int:projectid>/<int:suiteid>', methods=['GET'])
def suite_overview(suiteid, projectid):
    '''
    This call returns the aggregated results for a test suite within a project
    :param suiteid: int - existing suite id
    :param projectid: int - existing project id, the suiteid above should belong to this project.
    :return: 200 returns html page template and a variety of params to the template.
             500 if an error occurs
    '''
    try:
        dates, timeline, site_settings, project_desc = details_from_project_id(projectid)
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
                                   settings=site_settings, project_desc=project_desc)
        else:
            return '', 404
    except Exception, err:
        print err
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
    except Exception, err:
        print err
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
        site_settings = PrettySiteSettings.listsettings()
        data = {'version' : site_settings[0][1], 'name' : site_settings[1][1], 'api_tokens_enabled' : site_settings[2][1]}
        if data['api_tokens_enabled'] == 'True':
            if site_settings[3][0] == 'Key2':
                data['Key2'] = site_settings[3][1]
            if site_settings[3][0] == 'Key1':
                data['Key1'] = site_settings[3][1]
            if site_settings[4][0] == 'Key2':
                data['Key2'] = site_settings[4][1]
            if site_settings[4][0] == 'Key1':
                data['Key1'] = site_settings[4][1]
        return (str(json.dumps(data)), 200)
    except Exception, err:
        print err
        return ('', 500)

@app.route('/settings', methods=['POST'])
def update_settings():
    '''
    This call can be used to update the prettyunit settings. The second value in the tuple should always be "False" in order for this call to work.
    {
        "Name":[{string}, "False"],
        "API Tokens Enabled":[["True" or "False"], "False"]
    }
    :return: 200 if successful
             500 if there was an error
    '''
    try:
        content = request.get_json(silent=True)
        newKeys = {}
        for key, val in content.items():
            if val[1] == "False":
                PrettySiteSettings.setsettingvalue(key, val[0])
            if key == "Key1" or key == "Key2":
                newKeys[key] = val[0]
        keyHandler = APIKey()
        APIToken.replaceAPItoken(keyHandler.createMasterKey(newKeys["Key1"], newKeys["Key2"]))
        return '', 200
    except Exception, err:
        print err
        return '', 500



# -------------------------------- Results ------------------------------------------------
@app.route('/api/results', methods=['POST'])
def add_results():
    '''
    This call is used to add new test records to pretty unit. Currently it can accept the
    following formats [json v 1.0, ]
    ---------------------------- json v 1.0 --------------------------------------------------
    {
      "puv": "1.0",
      "tests-error": {integer},
      "tests-skipped": {integer},
      "timestamp": {string},
      "system": {string},
      "server": {string},
      "project": {string},
      "test-to-run": {integer},
      "tests-failure": {integer},
      "tests-run": {integer},
      "suite-name": {string},
      "test-cases": {
        "BaseTest1": [
          {
            "test-name": {string},
            "message": null or {string},
            "result": {string},
            "time": {float}
          }
        ]
      }
    }
    :return: 200 if call was successfully parsed
             400 if request body was determined to be malformed
             401 if API keys are enabled and request includes missing or incorrect keys
             500 if a server error occurs
    '''
    try:
        keygen = APIKey()
        useTokens = keygen.areTokensEnabledAndExist()
        if useTokens:
            keyHeader = request.headers.get('X-Keys')
            keys = json.loads(keyHeader)
            token = keygen.createMasterKey(keys["Key1"], keys["Key2"])
            if APIToken.validateToken(token):
                APIV = APIHandler()
                if request.headers.get('content-type') == 'application/json':
                    content = request.get_json(silent=True)
                    for i in range(0, len(content)):
                        if APIV.is_v1(content[i]):
                            # Parse Project
                            APIV.project_parser_v1(content[i])
                            # Parse Server
                            APIV.server_parser_v1(content[i])
                            # Parse Suite
                            APIV.suite_parser_v1(content[i])
                            # Parse TestCases and Tests
                            APIV.tests_parser_v1(content[i])
                        else:
                            return ('unsupported PU json version', 400)
                    return ('', 200)
                elif request.headers.get('content-type') == 'application/xml':
                    print 'xml request'
                    return ('xml support underway', 400)
                else:
                    return ('non-json format not yet supported', 400)
            else:
                return ('Invalid token', 401)
        else:
            APIV = APIHandler()
            if request.headers.get('content-type') == 'application/json':
                content = request.get_json(silent=True)
                for i in range(0, len(content)):
                    if APIV.is_v1(content[i]):
                        # Parse Project
                        APIV.project_parser_v1(content[i])
                        # Parse Server
                        APIV.server_parser_v1(content[i])
                        # Parse Suite
                        APIV.suite_parser_v1(content[i])
                        # Parse TestCases and Tests
                        APIV.tests_parser_v1(content[i])
                    else:
                        return ('unsupported PU json version', 400)
                return ('', 200)
            elif request.headers.get('content-type') == 'application/xml':
                print 'xml request'
                return ('xml support underway', 400)
            else:
                return ('non-json format not yet supported', 400)
    except Exception, err:
        print err
        print "still"
        return ('', 500)




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
    except Exception, err:
        print err
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
    except Exception, err:
        print err
        return ('', 500)




# -------------------------------- Project ------------------------------------------------
@app.route('/project/<int:projectid>', methods=['PUT'])
def update_project(projectid):
    '''
    This call can be used to update the details of an existing project.
    {
        'Project': {string},
        'Url': {string},
        'Description': {string},
        'Language': {string}
    }
    :param projectid: int - This should be the ID of an existing project.
    :return: 200 if successful
             404 if the project does not exist
             500 if there was an error
    '''
    if Project.does_exist(projectid):
        try:
            content = request.get_json(silent=True)
            Project.setprojectfields(projectid, content)
            return ('', 200)
        except Exception, err:
            print err
            return ('', 500)
    return ('', 404)

@app.route('/project/<int:projectid>', methods=['GET'])
def get_project(projectid):
    '''
    This call should return a json object with the details for an existing project.
    :param projectid: int - This should be the ID of an existing project.
    :return: 200 if successful
             404 if the project does not exist
             500 if there was an error
    '''
    if Project.does_exist(projectid):
        try:
            project = Project.getprojectdetails(projectid)[0]
            data = {'id' : project[0], 'name' : project[1], 'description' : project[2], 'language' : project[3], 'url' : project[4]}
            return (str(json.dumps(data)), 200)
        except Exception, err:
            print err
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
    except Exception, err:
        print err
        return ('', 500)



# -------------------------------- Helpers ------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def details_from_project_id(projectid):
    try:
        tl = Suite.timeline(projectid)
        site_settings = PrettySiteSettings.listsettings()
        project = Project.getprojectdetails(projectid)[0]
        project_desc = {'id' : project[0], 'name' : project[1], 'description' : project[2], 'language' : project[3], 'url' : project[4]}
        timeline = [[], [], [], []] # skip, error, fail, pass
        dates = []
        for t in tl:
            timeline[0].append(t[3])
            timeline[1].append(t[2])
            timeline[2].append(t[1])
            timeline[3].append(t[0])
            dates.append(t[4].strftime("%m/%d/%y %H:%M UTC"))
        return (dates, timeline, site_settings, project_desc)
    except:
        pass