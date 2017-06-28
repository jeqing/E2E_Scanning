import pypyodbc
from time import gmtime, strftime

def connectToDB(server, dataBase):
        con = pypyodbc.connect("DRIVER={SQL Server}; SERVER=" + server + ";DATABASE=" + dataBase + ";")
        
        return con

# check data in DB and populate a csv file with data with errors
def checkDataInDB(server, dataBase, tableName, docIdGuidList, fieldToCheck, errorLogLocation):
        currentDateTime = strftime("%Y%m%d_%H_%M_%S", gmtime())
        headers = ['censusMarkinStatusUid', 'censusMarkinStatus', 'documentNumber', 'salesforceMarkinStatusCode']


        errorLog = open(errorLogLocation + "MarkinErrorLog_" + currentDateTime + ".csv", "w")
      
        errorLog.write(','.join(headers) + '\n')
        
        con = connectToDB(server, dataBase)
        cursor = con.cursor()
        indexToCheckInDocIdGuidList = 0
        fieldToCheckInDB = ""
        if(tableName == "StatsNZ_ECP_Markin.dbo.CensusMarkinStatus"):
                indexToCheckInDocIdGuidList = 0     # use DocIds from docIdGuidList to search data in DB
                fieldToCheckInDB = "documentNumber" # look at the documentNumber field in DB
        elif(tableName ==  "StatsNZ_Epl_ResponseStore.data.response_image_PublicReport_v"):
                indexToCheckInDocIdGuidList = 1    # use Guids from docIdGuidList to search data in DB
                fieldToCheckInDB = "response_id"
        else:
                indexToCheckInDocIdGuidList = 1 
                fieldToCheckInDB = fieldToCheck              
                


        for docIdGuidTuple in docIdGuidList:  
                query = "select " + "censusMarkinStatusUid, censusMarkinStatus, documentNumber, salesforceMarkinStatusCode" + " from " + tableName +" where " + fieldToCheckInDB + "=" + "'" + docIdGuidTuple[indexToCheckInDocIdGuidList] + "'"
                queryResult = cursor.execute(query)
                fetchedResult = queryResult.fetchall()
                print (fetchedResult)
                
                for each in fetchedResult:
                        count = len(each)
                        i = 0
                        resultList = []
                        while (i < count):
                                resultList.append(str(each[i]))
                                i += 1
                        print(resultList)
                        errorLog.write(','.join(resultList)+ '\n') 
                      
                
   
        con.close()

    
        

checkDataInDB("wuatclsqlcorp10.stats.govt.nz", "StatsNZ_ECP_Markin", "StatsNZ_ECP_Markin.dbo.CensusMarkinStatus", [('642867781', 'abcd')], "salesforceMarkinStatusCode", "E:\\Testing\\Scanning E2E\\ErrorLogs\\")
#checkDataInDB("wuatclsqlcorp10.stats.govt.nz", "StatsNZ_Epl_ResponseStore", "StatsNZ_Epl_ResponseStore.data.response_image_PublicReport_v", [('123', 'badd7772-f92c-400f-b34a-bf4fda29f4ff')], "image_filename")
#checkDataInDB("wuatclsqlcorp10.stats.govt.nz", "StatsNZ_Epl_ResponseStore", "StatsNZ_Epl_ResponseStore.data.response_data_PublicReport_v", [('123', 'f2916d66-453d-4e74-bc40-b0df1526a638')], "questionnaire_id")