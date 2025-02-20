##################################################################################################################
# Main.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Main module to set up the configs and call the other moduels.
##################################################################################################################

import Gen_test_files
import Zipping
import Encryption
import datetime
import DbChecks
import CheckSalesForce
import EmailGeneration
import Setup
import time
import os
import FileTransfer_CK
from os.path import basename


# Configs for the variables used for Gen_test_files.py
sampleDataFolder = "C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\sample\\"
testDataFolder = "C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files\\"
#detailJsonFile = "UPDATE_20170411_10_04_55_214.json"
#detailJsonFile = "UPDATE_20170630_12_13_22_214.json"
folderPrefix = "IFC_UAT"


# Configs for the variables used for DbChecks.py
serverUAT = "wuatclsqlcorp10.stats.govt.nz"
#serverTest = 'snz-corp1-tst-sql'
db1 = "StatsNZ_ECP_Markin"
table1 = "StatsNZ_ECP_Markin.dbo.CensusMarkinStatus"
docIdGuidList1 = [('642867781', 'abcd'), ('642867781', 'abcd'), ('6428677812', 'abcd'), ('6428677813', 'abcd'), ('6428677813', 'abcd'), ('6428677813', 'abcd')]
fieldToIdentify1 = "documentNumber"
fieldToCheckInDB1 = "salesforceMarkinStatusCode"
valuetoCheckAgainst1 = "markedIna"
errorLogLocation1 = "E:\\Testing\\Scanning E2E\\ErrorLogs\\"
fieldsToSelectList1 = ['censusMarkinStatusUid', 'censusMarkinStatus', 'documentNumber', 'numberOfOccupants', 'salesforceMarkinStatusCode', 'createdDate']


db2 = "StatsNZ_Epl_ResponseStore"
table2 = "StatsNZ_Epl_ResponseStore.data.response_image_PublicReport_v"
docIdGuidList2 = [('123', 'badd7772-f92c-400f-b34a-bf4fda29f4ff'), ('123', 'badd7772-f92c-400f-b34a-bf4fda29f4fa')]
fieldToIdentify2 = "response_id"
fieldToCheckInDB2 = "image_filename"
valuetoCheckAgainst2 = ""
errorLogLocation2 = "E:\\Testing\\Scanning E2E\\ErrorLogs\\"
fieldsToSelectList2 = ['response_image_id', 'image_filename', 'create_date', 'response_id', 'collection_instance_id', 'document_set_id']


db3 = "StatsNZ_Epl_ResponseStore"
table3 = "StatsNZ_Epl_ResponseStore.data.response_data_PublicReport_v"
docIdGuidList3 = [('123', 'f2916d66-453d-4e74-bc40-b0df1526a638'), ('123', 'f2916d66-453d-4e74-bc40-b0df1526a630')]
fieldToIdentify3 = "questionnaire_id"
fieldToCheckInDB3 = ""
valuetoCheckAgainst3 = ""
errorLogLocation3 = "E:\\Testing\\Scanning E2E\\ErrorLogs\\"
fieldsToSelectList3 = ['response_data_id', 'questionnaire_id', 'create_date', 'response_id', 'collection_instance_id']


# Configs for the variables used for EmailGeneration.py
errorLogPath = "E:\\Testing\\Scanning E2E\\ErrorLogs"
subj = 'Scanned Images Error Notification'
sender = "stats.integration.testing@gmail.com"
recipients = ["christina.kim@stats.govt.nz", "jeqing@gmail.com", "christina.kim@assurity.co.nz"]
message = 'There is some data with errors.  Please find the attached files for the details'
server = "smtp.gmail.com"
port = 587
senderUserName = "stats.integration.testing@gmail.com"
senderPw = "Stats12345"




if __name__ == "__main__":
    #Remove test data files used from the previous run
    Setup.removeTestFiles("C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files")
    #Where zipped test data files are stored
    outputFile = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\current\\'
   
    gpg_output = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\gpg_files\\'
    #Where files to be zipped are picked up from
    fileToZip = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files\\'

    #Generate test data files
    docIdGuidList = Gen_test_files.generateTestFiles(sampleDataFolder, testDataFolder, folderPrefix, 1)
    ###Zip the generated test data files
    zippedFile = Zipping.archiveFolder(fileToZip)    
    
    Encryption.encryptFile(fileToZip,  "C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\")
    
    #FileTransfer_CK.transferFiles()
    
    ##Wait before checking the DBs
    #time.sleep(600)
    
    
    ##Check the data bases to see if the loaded test data files were processed as expected
    #DbChecks.executeQuery(serverUAT, db1, table1, docIdGuidList, fieldToIdentify1, fieldToCheckInDB1, valuetoCheckAgainst1, errorLogLocation1, fieldsToSelectList1)
    #DbChecks.executeQuery(serverUAT, db2, table2, docIdGuidList, fieldToIdentify2, fieldToCheckInDB2, valuetoCheckAgainst2, errorLogLocation2, fieldsToSelectList2)
    #DbChecks.executeQuery(serverUAT, db3, table3, docIdGuidList, fieldToIdentify3, fieldToCheckInDB3, valuetoCheckAgainst3, errorLogLocation3, fieldsToSelectList3)   
    #CheckSalesForce.checkDataInSalesForce('sunjeet81@gmail.com', 'yorks64&*', 'iKR2pcS09UvwRxMgaPcDjEi8', "SELECT Mark_In__c FROM Response__c WHERE Access_Code__c =", docIdGuidList, errorLogLocation1, ["DocID", "Guid", "MarkIn_Status"])
    
    ##Trigger an email with the error log files as an attachement if there was any issue found
    #EmailGeneration.generateEmailNotifications(errorLogPath, subj, sender, recipients, message, server, port, senderUserName, senderPw)

    