# Python_Apple_Store_API_Wrapper
Scrapping data from Apple app store using iTunes search API

Scraps all apps from app store on basis of seller name. Results can be filtered for false positives on the basis of seller url. Url will be checked if url is passed to function and url is recived from api, as some apps do not have seller url. If any of these urls are missing then url check will not be performed.

##Requirements
- Pandas
- Requests

##Usage
```
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
```
