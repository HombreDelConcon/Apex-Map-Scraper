import string
from bs4 import BeautifulSoup as bs
import requests
import re

#Fetch computer headers from httpbin.org/get
def _scrapeHeaders() -> str:
    url = "http://httpbin.org/get"
    site = requests.get(url)
    rawHTML = site.text

    soup1 = bs(rawHTML, 'lxml')
    soup2 = bs(soup1.prettify(), 'lxml')

    headers = soup2.find('p')
    string = headers.text

    return string

#Use regex to get AcceptEncoding header and return it in a tuple
def _getAcceptEncoding(html:str) -> tuple:
    try:
        acceptEncodingPattern = re.compile(r'("Accept-Encoding"): (".+")')
        matches = acceptEncodingPattern.search(html)

    except AttributeError:
        print('No matches for Accept Encoding')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None

#Use regex to get Accept header and return it in a tuple
def _getAccept(html:str) -> tuple:
    try:
        AcceptPattern = re.compile(r'("Accept"): (".+")')
        matches = AcceptPattern.search(html)

    except AttributeError:
        print('There are no matches for Accept')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None


#Use regex to get Host header and return it in a tuple
def _getHost(html:str) -> tuple:
    try:
        HostPattern = re.compile(r'("Host"): (".+")')
        matches = HostPattern.search(html)
    except:
        print('There are no matches for Host')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None


#Use regex to get UserAgent header and return it in a tuple
def _getUserAgent(html:str) -> tuple:
    try:
        UserAgentPattern = re.compile(r'("User-Agent"): (".+")')
        matches = UserAgentPattern.search(html)
    except:
        print('There are no matches for User Agent')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None


#Use regex to get AmzTrace header and return it in a tuple
def _getAmzTrace(html:str) -> tuple:
    try:
        amzTracePattern = re.compile(r'("X-Amzn-Trace-Id"): (".+")')
        matches = amzTracePattern.search(html)
    except:
        print('No matches found for AMZ trace')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None

#Use regex and return the AcceptLanguage header in a tuple 
def _getAcceptLanguage(html:str) -> tuple:
    try:
        AcceptLanguagePattern = re.compile(r'("Accept-Language"): (".+")')
        matches = AcceptLanguagePattern.search(html)
    except:
        print('No matches found for Accept Language')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None

#use regex and return the CacheControl header in a tuple 
def _getCacheControl(html:str) -> tuple:
    try:
        CacheControlPattern = re.compile(r'("Cache-Control"): (".+")')
        matches = CacheControlPattern.search(html)
    except:
        print('No matches found for Cache Control')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None

#Use regex and return the UpgradeInsecureRequests header in a tuple 
def _getUpgradeInsecureRequests(html:str) -> tuple:
    try:
        UpgradeInsecureRequestsPattern = re.compile(r'("Upgrade-Insecure-Requests"): (".+")')
        matches = UpgradeInsecureRequestsPattern.search(html)
    except:
        print('No matches returned for Upgrade Insecure Requests')
        return None
    else:
        if matches != None:
            return (matches.group(1), matches.group(2))
        return None



#Gather all the headers from all the different functions and return them all
#   in a dictionary 
def headerDict() -> dict:
    stringHTML = _scrapeHeaders()

    AE = _getAcceptEncoding(stringHTML)
    A = _getAccept(stringHTML)
    H = _getHost(stringHTML)
    UA = _getUserAgent(stringHTML)
    AT = _getAmzTrace(stringHTML)
    CC = _getCacheControl(stringHTML)
    AL = _getAcceptLanguage(stringHTML)
    UIR = _getUpgradeInsecureRequests(stringHTML)


    arrayOfHeaders = [AE, A, H, UA, AT, CC, AL, UIR]
    finalDict = {}

    for header in arrayOfHeaders:
        if header != None:
            finalDict.update({header[0]:header[1]})
            #print('%s: %s' % (header[0], header[1]))
    
    return finalDict
    
    #for key,value in finalDict.items():
    #    print('%s : %s' % (key, value))

    
if __name__ == '__main__':
    headerDict()
    #x = _scrapeHeaders()
    #print(x)
