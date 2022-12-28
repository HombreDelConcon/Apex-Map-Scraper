from apexMapScraper import ApexMapScraper
import sys
import getopt
import scraperExceptions as _se

def main():
    args = sys.argv[1:]
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


if __name__ == '__main__':
    main()
