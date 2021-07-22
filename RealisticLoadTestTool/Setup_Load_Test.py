# --------------------------------------------------
# Import libraries
# --------------------------------------------------
import os
import datetime
from shutil import copyfile
import re
import msal
import requests
import json
# --------------------------------------------------
# Variables declaration
# --------------------------------------------------
destinationDir = ''
workingDir = os.getcwd()

# --------------------------------------------------
# Create Directory for test case and copy master files into it
# --------------------------------------------------
final_directory = os.path.join(workingDir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

sourceToken = os.path.join(workingDir, 'PBIToken.json')
sourceReport = os.path.join(workingDir, 'PBIReport.json')
sourceHtml = os.path.join(workingDir, 'RealisticLoadTest.html')

destinationToken = os.path.join(final_directory, 'PBIToken.json')
destinationReport = os.path.join(final_directory, 'PBIReport.json')
destinationHtml = os.path.join(final_directory, 'RealisticLoadTest.html')

copyfile(sourceToken, destinationToken)
copyfile(sourceReport, destinationReport)
copyfile(sourceHtml, destinationHtml)

# --------------------------------------------------
# Update the working directory to the new created test folder
# --------------------------------------------------
path = os.path.abspath(final_directory)
os.chdir(path)
workingDir = os.getcwd()


# --------------------------------------------------
# Set Authentication variables for SP authentication
# --------------------------------------------------

client_id = '<INSERT CLIENT ID>'
client_secret = '<INSERT SP SECRET>'
authority_url = 'https://login.microsoftonline.com/<INSERT TENANT ID>'
scope = ["https://analysis.windows.net/powerbi/api/.default"]
url_groups = 'https://api.powerbi.com/v1.0/myorg/groups'

# --------------------------------------------------
# Get the access token via SP authentication
# --------------------------------------------------

app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority_url,
    client_credential=client_secret)

result = app.acquire_token_for_client(scopes=scope)

accessToken = result['access_token']


# --------------------------------------------------
# Get the workspaces list
# --------------------------------------------------
header = {'Content-Type': 'application/json', 'Authorization': f'Bearer {accessToken}'}
api_out_w = requests.get(url=url_groups, headers=header)
workspacesJson = api_out_w.json()

workspacesId = []
workspacesName = []
workspaces = {}

for w in workspacesJson['value']:
    workspacesId.append(w['id'])
    workspacesName.append(w['name'])

workspaces['id'] = workspacesId
workspaces['name'] = workspacesName

groupName = workspaces['name'][0]  # for demo purposes forcing to choose the first workspace
groupId = workspaces['id'][0]  # for demo purposes forcing to choose the first workspace id

print('Got the workspace info, workspaceName:', groupName,  ',workspaceId: ', groupId)

# -------------------------------------------------
# Get the reports list
# --------------------------------------------------
header = {'Content-Type': 'application/json', 'Authorization': f'Bearer {accessToken}'}
api_out_r = requests.get(url=f'https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports', headers=header)
reportsJson = api_out_r.json()


reportsId = []
reportsName = []
reportsEmbedUrl = []
reportsDataset = []
reports = {}

for r in reportsJson['value']:
    reportsId.append(r['id'])
    reportsName.append(r['name'])
    reportsEmbedUrl.append(r['embedUrl'])
    reportsDataset.append(r['datasetId'])

reports['id'] = reportsId
reports['name'] = reportsName
reports['embedUrl'] = reportsEmbedUrl
reports['datasetId'] = reportsDataset

reportId = reports['id'][0] # for demo purposes forcing to choose the first report id
reportDataset = reports['datasetId'][0] # for demo purposes forcing to choose the first report dataset
reportName = reports['name'][0] # for demo purposes forcing to choose the first report
reportEmbedUrl = reports['embedUrl'][0]  # for demo purposes forcing to choose the first reportEmbedUrl

print('Got the report info, reportName:', reportName, ',reportId:', reportId, ',reportsDataset:',
      reportDataset, ',reportEmbedUrl:', reportEmbedUrl)

# -------------------------------------------------
# Generate Embed Token
# --------------------------------------------------

api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'

body = {"datasets": [{"id":  f'{reportDataset}'}], "reports": [{"allowEdit": True, "id": f'{reportId}'}],
        "targetWorkspaces": [{"id": f'{groupId}'}]}

headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {accessToken}'}

response = requests.post(api, json=body, headers=headers)
embedToken = response.json().get('token')

# --------------------------------------------------
# Create tokenExpiration file
# --------------------------------------------------
expiration = response.json().get('expiration')
tokenExpiration = json.dumps(expiration)
jsonFile = open("tokenExpiration.json", "w")
jsonFile.write(tokenExpiration)
jsonFile.close()

# --------------------------------------------------
# Update Token File
# --------------------------------------------------
with open("PBIToken.json", "r") as tokenJSONFile:
    dataToken = tokenJSONFile.read()  # returns a string

token_regex = r"(?<=PBIToken\":\").*?(?=\")"

dataToken = re.sub(token_regex, embedToken, dataToken)

with open("PBIToken.json", "w") as tokenJSONFile:
    tokenJSONFile.write(dataToken)

print('Updated Token File')


# --------------------------------------------------
# Update Report File
# --------------------------------------------------
with open("PBIReport.json", "r") as reportJSONFile:
    dataReport = reportJSONFile.read()  # returns a string

reportUrlRegex = r"(?<=reportUrl\":\s\").*?(?=\")"

dataReport = re.sub(reportUrlRegex, reportEmbedUrl, dataReport)

with open("PBIReport.json", "w") as reportJSONFile:
    reportJSONFile.write(dataReport)

print('Updated Report File')
print('Process Ended')
