###################################################################################################################################
# This scripts uses a Python package called "simple salesforce" to connect to salesforce and use the Salesforce query language 
# i.e. very similar to SQL and then traverses the response data strcture to print the Mark in status for an access code in salesforce 
# create by Ben,Christina and Sunjeet 14th June,2017
####################################################################################################################################


#Simple salesforce package that is being used for this Test script 
from simple_salesforce import Salesforce

# connect to salesforce sandbox ( regression ) envrionment , using desired user name and password AND secuirty-token that can be retrieved from that SF instance --> 
# (under you user name) "my settings" hyperlink --> "personal" --> "reset my security token"

sf = Salesforce(username='sunjeet81@gmail.com', password='yorks64&*', security_token='iKR2pcS09UvwRxMgaPcDjEi8', sandbox=True)


# run a SOQL query to select the mark in value from a response salesforce object , for a particular access code
# the documentation for exposed APIs can be found in Salesforce from set up --> Build --> create --> Objects 
result = sf.query_all("SELECT Mark_In__c FROM Response__c WHERE Access_Code__c ='169917636MPY'")


# the SOQL query returns an ordered  of nested dictionaries and a list
print(result)

#Christina's handy dandy solution to iterate through the returned data structure and output the value of the Mark in field for the access code 

#Get the records dictionary , because that is where the Mark in status values lies 
record = (result['records'])
print(record)

# ah ..ok records is not really a dictionary but a list because it has not got sqaure brackets around it , unlike e.e. what we get when we do "print(results)" 
# and it is a list with just one item so....get the first index of the list , which is a dictionary and store it in a variable
an_dict = record[0]
print(an_dict)

# print the value of the mark_In__C key
print (an_dict['Mark_In__c'])
