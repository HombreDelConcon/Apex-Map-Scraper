from apexMapScraper import ApexMapScraper
import sys
import getopt
import scraperExceptions as _se
import time
import subprocess

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
    headparam = None
    auth = None
    sid = None
    dnums = None
    snum = None

    #Define program behaviour when different options are passed into the first parameter
    try:
        argumentLis, valueLis = getopt.getopt(args, options, long_options)
        for arg, value in argumentLis:
            if arg in ('-h', '--help'):
                try:
                    with open('helpFile.txt') as f:
                        content = f.read()
                        print(content)
                        f.close()
                    return
                except:
                    print('Help file could not be found')
            elif arg in ('-b', '--background'):
                headless = True
                headparam = arg
            elif arg in ('-f', '--front'):
                headless = False
                headparam = arg
            print('passing parameters...')
    except:
        raise _se.ArgumentException('Error in the first parameter')

    #Map each parameter to its corresponding variable
    try:
        auth = sys.argv[2]
        sid = sys.argv[3]
        dnums = sys.argv[4]
        snum = sys.argv[5]
    except:
        raise _se.ArgumentException('Error in one of the parameters. Maybe not enough parameters? Consult the -h page for instructions')

    #Event loop which will run the scraper in either headless or front mode
    if headless == False:
        print('starting scraper in front mode')
        scraper = ApexMapScraper(auth_token=auth, acc_sid=sid, source=snum, targets=dnums, terminal=headparam)
    else:
        print('Starting scraper in headless mode')
        try:
            subprocess.run(['pyw', 'apexMapScraperHeadless.pyw', headparam, auth, sid, dnums, snum])
        except:
            print('apexMapScraperHeadless.pyw could not be found')

if __name__ == '__main__':
    main()
