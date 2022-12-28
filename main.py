from apexMapScraper import ApexMapScraper
import sys
import getopt
import scraperExceptions as _se
import time

def main() -> None:

    #Take all the parameters passed in from cmd except for the first one which is the name of the program
    args = sys.argv[1:]

    #This is just checking the length of the list of arguments provided
    if len(args) < 5:
        raise _se.ArgumentException('There are not enough parameters passed in')
    
    #Define the different options available
    options = 'hbf'
    long_options = ['help', 'background', 'front']

    headless = False
    auth = None
    sid = None
    dnums = None
    snum = None

    #Define program behaviour when these options are called
    try:
        argumentLis, valueLis = getopt.getopt(args, options, long_options)

        for arg, value in argumentLis:
            if arg in ('-h', '--help'):
                with open('helpFile.txt') as f:
                    content = f.read()
                    print(content)
                    f.close()
                return
            
            elif arg in ('-b', '--background'):
                headless = True
            
            elif arg in ('-f', '--front'):
                print('passing parameters...')
                pass
                
    except:
        raise _se.ArgumentException('Error in the first parameter')

    #Map each parameter to its corresponding value
    try:
        auth = sys.argv[2]
        sid = sys.argv[3]
        dnums = sys.argv[4]
        snum = sys.argv[5]
    
    except:
        raise _se.ArgumentException('Error in one of the parameters. Maybe not enough parameters? Consult the -h page for instructions')

    #Event loop which will run the scraper and constantly chech the time 
    scraper = ApexMapScraper(auth_token=auth, acc_sid=sid, source=snum, targets=dnums, noterminal=headless)
    times = scraper.activeTime()
    if not headless:
        print('starting event loop...')
    while True:
        if scraper.activateSequence(times):
            try:
                x = scraper.getCurrMap()
            except:
                if not headless:
                    print('Something Went wrong')
                pass
            else:
                scraper.sendMessage(x)
                time.sleep(10)
        time.sleep(1)

if __name__ == '__main__':
    main()
