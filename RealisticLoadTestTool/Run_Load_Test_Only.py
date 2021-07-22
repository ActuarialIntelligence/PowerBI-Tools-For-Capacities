# --------------------------------------------------
# Import libraries
# --------------------------------------------------
import os
import webbrowser
import psutil
import json
from datetime import datetime
from dateutil import tz

# --------------------------------------------------
# Return the number of CPUs in the system
# --------------------------------------------------

numberOfPhysicalCores = psutil.cpu_count(logical = False)
print("Note that each browser process requires about 1-2GB RAM!")
print('numberOfPhysicalCores:', numberOfPhysicalCores)

# --------------------------------------------------
# Check current working directory
# --------------------------------------------------
workingDir = os.getcwd()
print(workingDir)

# --------------------------------------------------
# Get the list of directories that have a .html file
# --------------------------------------------------


def getDirectoryList(path):
    directoryList = []

    # return nothing if path is a file
    if os.path.isfile(path):
        return []

    # add dir to directorylist if it contains .html files
    if len([f for f in os.listdir(path) if f.endswith('.html')])>0:
        directoryList.append(path)

    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            directoryList += getDirectoryList(new_path)

    return directoryList


foldersList = getDirectoryList(workingDir)
print(foldersList)
# --------------------------------------------------
# Update the working directory to the newest created test folder
# --------------------------------------------------
latestFolder = max(foldersList)
path = os.path.abspath(latestFolder)
os.chdir(path)
workingDir = os.getcwd()
print(workingDir)

# --------------------------------------------------
# Check token expiration datetime
# --------------------------------------------------

# Opening JSON file
tokenExpirationJSONFile = open('tokenExpiration.json', )

# returns JSON object as a dictionary
tokenExpiration = json.load(tokenExpirationJSONFile)
# Closing file
tokenExpirationJSONFile.close()

# Auto-detect zones:
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

now = datetime.now()
utcz = datetime.strptime(tokenExpiration, '%Y-%m-%dT%H:%M:%SZ')

# Tell the datetime object that it's in UTC time zone since
# datetime objects are 'naive' by default
utcz = utcz.replace(tzinfo=from_zone)
now = now.replace(tzinfo=to_zone)

# Convert time zone
localExpirationDate = utcz.astimezone(to_zone)
print(localExpirationDate)
print(now)

# --------------------------------------------------
# Enter number of instances to initiate for each report
# --------------------------------------------------
instances = 2

# --------------------------------------------------
# Run the html file
# --------------------------------------------------
for instance in range(instances):
    for file in os.listdir(workingDir):
        if file.endswith(".html"):
            #  print(os.path.join(workingDir, file))
            file = os.path.join(workingDir, file)
            new = 2  # open in a new tab
            url = 'file://' + os.path.realpath(file)
            webbrowser.open(url, new=new)


if now > localExpirationDate:
    print('The token is expired, closing all the tabs')
    os.system("taskkill /F /IM msedge.exe")
else:
    print('The Realist Load Testing Tool is running')
