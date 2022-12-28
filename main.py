from apexMapScraper import ApexMapScraper
import sys
import getopt
import scraperExceptions as _se
import time

def main() -> None:
    args = sys.argv[1:]

    if len(args) < 5:
        raise _se.ArgumentException('There are not enough parameters passed in')

    options = 'hbf'
    long_options = ['help', 'background', 'front']

    headless = False
    auth = None
    sid = None
    dnums = None
    snum = None

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
                pass

    except:
        raise _se.ArgumentException('Error in the first parameter')

    try:
        auth = sys.argv[2]
        sid = sys.argv[3]
        dnums = sys.argv[4]
        snum = sys.argv[5]
    
    except:
        raise _se.ArgumentException('Error in one of the parameters. Maybe not enough parameters? Consult the -h page for instructions')

    scraper = ApexMapScraper(auth_token=auth, acc_sid=sid, source=snum, targets=dnums, noterminal=headless)

    times = scraper.activeTime()

    while True:
        if scraper.activateSequence(times):
            try:
                x = scraper.getCurrMap()
            except:
                print('Something Went wrong')
                pass
            else:
                scraper.sendMessage(x)
                time.sleep(10)
        time.sleep(1)

if __name__ == '__main__':
    main()
