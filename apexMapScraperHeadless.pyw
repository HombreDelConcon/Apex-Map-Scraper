from bs4 import BeautifulSoup
import requests
import os
from twilio.rest import Client
import time
from headers import headerDict
import scraperExceptions as _se
import sys
import logging

class ApexMapScraper:

    def __init__(self, *argv, **kwargs) -> None:
        self._auth_token:str = None
        self._acc_sid:str = None
        self._target_numbers:list[str] = None
        self._source_number:str = None
        self._headless:bool = False

        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='%(levelname)s:%(message)s', filemode='w')

        try:
            self._auth_token = kwargs['auth_token']
            self._acc_sid = kwargs['acc_sid']
        except:
            self.logError('Must pass in both an API key and account SID')
            raise _se.ArgumentException('Must pass in both an API key and an account SID\nrun the -h command for details')
        
        try:
            self._target_numbers = kwargs['targets']
            self._source_number = kwargs['source']
        except:
            self.logError('One or both phone number(s) is/are missing')
            raise _se.ArgumentException('One or both phone number(s) is/are missing\nrun the -h command for details')
        else:
            tempArr = []
            with open(self._target_numbers) as t:
                for line in t:
                    tempArr.append(line)
                t.close()
            self._target_numbers = tempArr
        
        try:
            if kwargs['terminal'] in ('-b', '--background'):
                self._headless = True
            elif kwargs['terminal'] in ('-f', '--front'):
                pass
            else:
                raise _se.ArgumentException('%s is not recognized as a mode' % (kwargs['terminal'], ))
        except Exception as e:
            self.logWarning(str(e))
            raise _se.ArgumentWarning(str(e))
        
        #Type checking each of the passed in parameters
        for arg in (kwargs['auth_token'], kwargs['acc_sid'], kwargs['source'], kwargs['terminal']):
            if type(arg) != str:
                self.logError('Parameter not of the correct type')
                raise _se.ArgumentException('Parameters not of the correct type')
        
        for target in self._target_numbers:
            if type(target) != str:
                self.logError('Phone number in list is not of the string type')
                raise _se.ArgumentException('Phone number in list is not of the string type')

        #Testing to make sure that all of the correct parameters were passed in
        if not self._headless:
            print('All parameters  passed')
            self.logInfo('All parameters passed in successfully')
            print('acc_sid: %s\nauth_token: %s\n' % (self._acc_sid, self._auth_token))
            print('target numbers:\n')
            for number in self._target_numbers:
                print('- %s' % (number,))
            print('source number: %s' % (type(self._source_number), ))
            print('In front mode')
            self.logInfo('Running scraper in front mode')
            try:
                self.frontloop()
            except:
                self.logError('Error while running web scraper in front mode')
        else:
            self.logInfo('Running scraper in headless mode')
            try:
                self.headlessloop()
            except:
                self.logError('Error while running scraper in headless mode')


    #Gets the current map in rotation and returns a tuple with the current map and the time it's going to be on for
    def getCurrMap(self) -> tuple:

        #Stores the URL
        link:str = 'https://apexlegendsstatus.com/current-map'

        #Stores HTTP headers
        HEADERS:dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7", "Upgrade-Insecure-Requests": "1", "X-Amzn-Trace-Id": "Root=1-6292aed6-1f65c2db636f27cb7ebcb533"}
        updatedHeaders = headerDict()
        HEADERS.update(updatedHeaders)

        #Makes a request to get the HTML from the URL
        html = requests.get(link, headers=HEADERS)

        #Stores and cleans the HTML of the webpage requested
        soup = BeautifulSoup(html.content, 'lxml')
        soup2 = BeautifulSoup(soup.prettify(), 'lxml')

        #Gets container with the name of the map in rotation
        map_ = soup2.find('div', {'class':'col-lg-8 olympus'})

        #Searches the container for a string representing the name of the map
        curr_map = map_.find('h1').get_text().strip()
        curr_map = curr_map[15:]

        #Stores the container with the time span the map will be available for
        timeContainer = soup2.find_all('span')

        #The website stores the time tags of many different maps but we only want the time for the
        #   current map and so we get all the tags into an array but only really care about the start
        #   and end times for the current map which are in the indexes 2 and 3 respectively
        timeLis = []
        for elemTime in timeContainer:
            timeLis.append(elemTime.get_text().strip())

        from_time = timeLis[2]
        to_time = timeLis[3]
        from_time = self.transValues(from_time)
        to_time = self.transValues(to_time)
        
        timeSpan = '%s a %s' % (from_time, to_time)

        return(curr_map, timeSpan)

    #There's a bunch of extra stuff we don't want with the tags storing the time so we are just getting rid
    #   of those. This is for EST time since working with time zones = messy
    def transValues(self, value:str) -> str:
        other_half = value[2:]

        #This scraper only really translates into eastern time, sorry :(
        num = str(int(value[:2]) - 4) # <---- that little -4 there specifies how many hours to take
        return num + other_half

    #If the current map is World's Edge then it sends a message to the phone numbers 
    #   specified in the attribute
    def sendMessage(self, val:tuple) -> bool:
        if val[0] == "World's Edge":
            try:
                account_sid = os.environ['TWILIO_ACCOUNT_SID']=self._acc_sid
                auth_token = os.environ['TWILIO_AUTH_TOKEN']=self._auth_token
                client = Client(account_sid, auth_token)
                bodyParam = '---------------------------------------Worlds Edge is out %s' % val[1]
                recipients = self._target_numbers
                for number in recipients:
                    message = client.messages.create(
                                body= bodyParam,
                                from_=self._source_number,
                                to=number
                                )
                
            except Exception as e:
                print('Could not send message')
                print(str(e))
                return False

            else:
                print('Message sent')
                return True
        else:
            timeNow = time.asctime()
            print('Map not in yet | Time: ' + timeNow)
            return False

    #This function will create a list of all the times at which we activate the web scraper which is set to 
    #   every half hour. This is the one bit of code I am not proud of because I know there must be a more
    #   efficient way of getting all the times I want without having to do all this.
    def activeTime(self) -> list[str]:
        activateTimes0to9 = ['0' + str(i) + ':00:00' for i in range(10)]
        activateTimes10to23 = [activateTimes0to9.append(str(i) + ':00:00') for i in range(10, 24)]
        activateTimes30mins = [activateTimes0to9.append(str(i) + ':30:00') for i in range(10, 24)]
        activateTimes30minsBelow10 = [activateTimes0to9.append('0' + str(i) + ':30:00') for i in range(10)]
        #activateTimes0to9.append('06:52:20')
        finalTimes = activateTimes0to9
        return finalTimes

    #This will determine whether it is time to activate the scraper
    def activateSequence(self, times:list) -> bool:
        timeLis = times
        curr_time = time.asctime()
        curr_time = curr_time[11:19]
        if curr_time in timeLis:
            return True
        return False

    #--------------------LOOPING FUNCTIONS----------------------------------------

    #When we are running the web scraper in front mode it will run this sequence
    def frontloop(self) -> None:
        y = self.activeTime()
        print('Starting scraper in terminal display mode...')
        print('Scraper will run at the following times:')
        for t in y:
            print(' - %s' % (t,))
            print()
        while True:
            if self.activateSequence(y):
                try:
                    x = self.getCurrMap()
                except:
                    break
                else:
                    self.sendMessage(x)
                    print('Message sent')
            time.sleep(1)
    
    #We run this when we want to run the scraper in headless mode. Why a whole nother function 
    #   that does basically the same thing but without printing? Isn't it better just to add
    #   conditions to the first loop function? Well 
    def headlessloop(self) -> None:
        y = self.activeTime()
        while True:
            if self.activateSequence(y):
                try:
                    x = self.getCurrMap()
                except:
                    break
                else:
                    self.sendMessage(x)
            time.sleep(1)
    
    #----------------------LOGGING FUNCTIONS-----------------------------------
    def getTime(self) -> str:
        now = time.strftime('%H:%M:%S', time.gmtime())
        return now
    
    def logError(self, message:str) -> bool:
        fullMsg = '(%s): %s' % (self.getTime(), message)
        logging.error(fullMsg)
        return True
    
    def logInfo(self, message:str) -> bool:
        fullMsg = '(%s): %s' % (self.getTime(), message)
        logging.info(fullMsg)
        return True
    
    def logDebug(self, message:str) -> bool:
        fullMsg = '(%s): %s' % (self.getTime(), message)
        logging.debug(fullMsg)
        return True
    
    def logWarning(self, message:str) -> bool:
        fullMsg = '(%s): %s' % (self.getTime(), message)
        logging.warning(fullMsg)
        return True

if __name__ == '__main__':

    auth = sys.argv[2]
    sid = sys.argv[3]
    targets = sys.argv[4]
    source = sys.argv[5]
    terminal = sys.argv[1]

    scraper = ApexMapScraper(auth_token=auth, acc_sid=sid, targets=targets, source=source, terminal=terminal)

