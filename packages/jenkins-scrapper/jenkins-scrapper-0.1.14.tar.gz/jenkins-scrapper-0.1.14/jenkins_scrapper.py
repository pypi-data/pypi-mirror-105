
import requests
import bs4
import configparser
import logging
import urllib3
import getopt
import sys
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

short_options = "hs:b:"
long_options = []

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))
#config.read('config.ini')
argToConfigMap = {
    'cc': 'ipc3controlcenter',
    'pc': 'ipc3paymentcontroller',
    'pos': 'ipc3pointofsale'
}
buildStatus = 'FAILED'
proxyDict = {
    "http": config.get('jenkins', 'httpProxy'),
    "https": config.get('jenkins', 'httpsProxy'),
    "ftp": config.get('jenkins', 'ftpProxy')
}

reqHeaders = {'Authorization': config.get('jenkins','authHeader')}
serviceUrl = ''
jenkinsBranch = 'develop'

def validateCmdLineArgs(argument_list, short_options, long_options):
    global serviceUrl
    global jenkinsBranch

    try:
        arguments = getopt.getopt(argument_list, short_options, long_options)
        #print(arguments)
        for arg in arguments:
            for arg1 in arg:
                if '-b' in arg1:
                    jenkinsBranch = str(arg[1][1])
                    if jenkinsBranch.__contains__('/'):
                        jenkinsBranch = jenkinsBranch.replace('/', '%2F')                
                elif '-s' not in arg1:
                    raise Exception('Mandatory arg -s not provided')
            
            # if '-b' in arg:
                
            #     jenkinsBranch = str(arguments[1][1])
            #     if jenkinsBranch.__contains__('/'):
            #         jenkinsBranch = jenkinsBranch.replace('/', '%2F')                
            # elif '-s' not in arg:
            #     raise Exception('Mandatory arg -s not provided')

   
    # Evaluate given options
        for current_argument in arguments:
            for arg in current_argument:
                if arg[0] in ("-s", "--service"):
                    serviceUrl = config.get('jenkins', argToConfigMap.get(arg[1]))
                    serviceUrl = serviceUrl.format(branch=jenkinsBranch)
            
    except getopt.error as err:
        # Output error, and return with an error code
        error = str(err)
        print(f"{bcolors.FAIL}{error}{bcolors.ENDC}")
        sys.exit(2)
    except Exception as err:
        # Output error, and return with an error code
        error = str(err)
        print(f"{bcolors.FAIL}{error}{bcolors.ENDC}")
        sys.exit(2)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


validateCmdLineArgs(argument_list, short_options, long_options)


response = requests.get(serviceUrl,
                        headers=reqHeaders,
                        proxies=proxyDict,
                        verify=False)
soup = bs4.BeautifulSoup(response.text, "lxml")

title = str(soup.select('title')[1].getText())
greenBuildFilters = config.get('jenkins', 'greenBuildFilters').split(',')

for greenBuildFilter in greenBuildFilters:
    if title.__contains__(greenBuildFilter.strip()):
        buildStatus = 'SUCCESS'
        break
if buildStatus.__eq__('SUCCESS'):
    print(f"{bcolors.OKGREEN}{buildStatus}{bcolors.ENDC}")
else:
    print(f"{bcolors.FAIL}{buildStatus}{bcolors.ENDC}")