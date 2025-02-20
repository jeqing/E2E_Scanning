
##################################################################################################################
# Gen_test_files.py
##################################################################################################################
# Author: Ben Schluter
# Date: 15 May 2017
# Description: Duplicate test input folders a specified number of times, modifying the folder JSON files
# as well as appending a form type record to the detail JSON file, both with new GUIDs for testing
##################################################################################################################

import os
import shutil
import uuid
import sys
from glob import glob
import datetime

def generateTestFiles():

# Modify below parameters for testing
# Escape \ characters in paths with a leading \
    testDataFolder = "C:\\Users\\Christina\\Desktop\\Stats\\E2E_Scanning\\Performance Test\\"
    detailJsonFile = "UPDATE_20170411_10_04_55_214.json"
    folderPrefix = "IFC_UAT"

    numberOfDuplicates = 1
    #outputJsonFile = "UPDATE_20170523_12_13_22_214.json"
    outputJsonFile = 'UPDATE_'+ datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S_214') + '.json'

    # Check test Data folder exists
    if not (os.path.isdir(testDataFolder)):
        print "Error: Test data Folder: " + testDataFolder + " not found!"
        sys.exit(1)

    # Check detail JSON file exists
    if not (os.path.isfile(testDataFolder + detailJsonFile)):
        print "Error: Detail JSON File: " + detailJsonFile + " not found!"
        sys.exit(1)

    # Retrieve all test image folders
    os.chdir(testDataFolder)
    folderList = glob(folderPrefix + "*\\")

    # Check there are test image folders present
    if len(folderList) == 0:
        print "Error: No test folders of prefix: " + folderPrefix + " found!"
        sys.exit(1)

    # Get last folder suffix used for test folders
    iter = 0

    for folder in folderList:
        intSuffix = int(folder[len(folderPrefix):len(folder)-1])
        if (intSuffix > iter):
            iter = intSuffix

    # Read in Detail Json file to memory, remove last closing brace
    detailJson = open(detailJsonFile,"r")
    detailLine = detailJson.read()
    detailJson.close()
    lenOrig = len(detailLine)
    finalJson = detailLine[:lenOrig-1]

    # For number of test duplicates
    for i in range(numberOfDuplicates):
        # For each test image folder
        for j in range(len(folderList)):
            # Increment the folder suffix
            iter = iter + 1
            i_str = str(iter).strip()

            # Copy the image folder to the new folder
            shutil.copytree(testDataFolder + folderList[j], testDataFolder + folderPrefix + i_str)

            # Get current test folder removing the trailing folder separator
            currFolderTmp = folderList[j]
            currFolder = currFolderTmp[:len(currFolderTmp)-1]

            # Read in the folder JSON file
            json = open(testDataFolder + folderPrefix + i_str + "\\" + currFolder + ".json","r")
            origLine = json.read()
            json.close()

            # Remove the folder JSON file
            os.remove(testDataFolder + folderPrefix + i_str + "\\" + currFolder + ".json")

            imageFolderList = os.listdir(testDataFolder + folderPrefix + i_str)
            itemList = []

            # Find all tif image files in the folder
            for file in imageFolderList:
                if file.find(".tif") > 0:
                    itemList.append(file)

            # CK: Write a file with GUI IDs used
            #fOpen = open('C:/Users/Christina/Desktop/Stats/E2E_ScanningDocIDs_GUIs.csv', 'w')
            
            # For each image
            for item in itemList:
                # Generate new GUID
                newId = uuid.uuid4()
                
                #fOpen.write(str(newId)) #CK

                newName = str(newId) + item[36:]
                # Rename the image file
                os.rename(testDataFolder + folderPrefix + i_str + "\\" + item,testDataFolder + folderPrefix + i_str + "\\" + newName)

                oldId = item[0:36]

                # Replace GUID in the folder JSON file
                newLine = origLine.replace(oldId, str(newId))
                origLine = newLine

                # Find the form type record for the old GUID from the detail JSON file
                startPos = detailLine.find(oldId)
                if (startPos == -1):
                    print "Error: GUID " + oldId + " not found in detail JSON file"
                    sys.exit(1)

                checkFrom = startPos - 50
                if (checkFrom < 0):
                    checkFrom = 0

                startPosAll = detailLine.find("{\"form_type\":",checkFrom)
                startPosFin =  detailLine.find("{\"form_type\":",startPos)
                if startPosFin == -1:
                    startPosFin = len(detailLine)

                relText = detailLine[startPosAll:startPosFin-1]
                relText2 = relText.replace(oldId, str(newId))

                finalJson2 = finalJson + "," + relText2
                finalJson = finalJson2

            #fOpen.close() #CK
            
            newJson = open(testDataFolder + folderPrefix + i_str + "\\" + folderPrefix + i_str + ".json","w")
            newJson.write(origLine)
            newJson.close()

    finalJson2 = finalJson + "]"
    finalJson = finalJson2

    newFinalJson = open(testDataFolder + outputJsonFile,"w")
    newFinalJson.write(finalJson)
    newFinalJson.close()


generateTestFiles()