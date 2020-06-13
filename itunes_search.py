import requests
import pandas as pd
import json
import sys

def getApiResults(companyName, companyUrl = ''):
    #fetch results from itunes api
    tempFrame = pd.DataFrame()
    url = "https://itunes.apple.com/search"
    resultLimit = 200 #api limit range 1-200
    countryCode = 'US' #country store to query

    payload = {'term' : companyName, 'country' : countryCode, 'media' : 'software', 'limit' : resultLimit}

    try:
        req = requests.get(url, params=payload)
        print("Fetching data for >> " + companyName)
        res = json.loads(req.text)
        print("Extracting data")
        for item in res['results']:
            #extract and append information for each app for this comapny to data frame, one per row
            extData = extractData(item)
            if(companyName.lower() in extData['sellerName'][0].lower()): #append only if company name matches the seller name of app
                if(companyUrl != ''): #check if company url was entered in input file
                    try:
                        companyURL_fromApi = extData['sellerUrl'][0].lower() #this will throw exception if sellerUrl not received from api
                        if(companyUrl.strip() in companyURL_fromApi):
                            #append results
                            tempFrame = tempFrame.append(extData)
                        else:
                            #continue without appending as url was not found
                            continue
                    except:
                        #url not received from api, append without checking url
                        tempFrame = tempFrame.append(extData)
                        continue
                else:
                    #append resuls
                    tempFrame = tempFrame.append(extData)

    except requests.exceptions.RequestException as e:
        print('API Error')
        raise SystemExit(e)
    except BaseException as error:
        sys.exit('An exception occurred: {}'.format(error))


    return tempFrame

def extractData(data):
    temp = pd.DataFrame()
    for item in data:
        if isinstance(data[item], list):
            temp[item] = [', '.join(data[item])] #convert list of strings to one string and place in frame
        else:
            temp[item] = [data[item]]
    return temp


def compileData_list(listOfCompanies_url):
    #use function to get data from a list of companies
    mainFrame = pd.DataFrame() # dataframe to hold all results

    for pair in listOfCompanies_url:
        companyName = pair[0]
        companyUrl  = pair[1]
        apiResults = getApiResults(companyName, companyUrl)
        mainFrame = mainFrame.append(apiResults) #append results to main frame

    return mainFrame


def test():
    #get data from list of companies
    input_list = [ ['google', 'google.com'], ['dnb', 'dnb.no'], ['walmart', '']]
    results_list = compileData_list(input_list)

    print("Writing results from list of comapnies to file")
    results_list.to_csv('results_list.csv')
    print("Done")

    #get data from single company
    results_single = getApiResults('walmart')
    print("Writing results of single company without url to file")
    results_single.to_csv('results_single_without_url.csv')
    print("Done")

    #results with url
    results_single = getApiResults('walmart', 'walmart.com')
    print("Writing results of single company with url to file")
    results_single.to_csv('results_single_with_url.csv')
    print("Done")

test()
