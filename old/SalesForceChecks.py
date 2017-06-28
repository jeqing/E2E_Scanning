from simple_salesforce import Salesforce


def checkDataInSalesForce(user, pw, token):
    sf = Salesforce(username = user, password = pw, security_token = token, sandbox = True)
    user = sf.User.get("abcd")
    
    print(user)
    
    result = sf.query_all("select Id, Email from User where LastName = 'Kim'")
    
    print("\n\nResult:\n=====\n")
    print(result)
    
    

