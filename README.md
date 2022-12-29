# Apex-Map-Scraper
Description: This is a web scraper to find the current map in the Apex Legends public lobby. This scraper has not been tested to work on iMac nor Linux. This scraper is running on Python 3.10.4 so it may or may not run on other versions.

Please run this program in a virtual environment as it may require some libraries which are not available or run on different versions of already installed libraries. A requirements.txt file is included which you can just pass into pip. 

Instructions: First thing to do is to make sure you have a Twilio account as we are going to be using their service to send the text messages. Creating an account is free and they give you a trial number and enough trial money to send A LOT of messages. Sending messages only costs a few pennies so the trial money should be enough so long as you are not running like 50 simultaneous instances of this program. Make sure you have the phone numbers you are going to be using be confirmed in your Twilio account (yes you need to this).

To get started you will need to pass in parameters to the main program, this isone from the command line.

Options:

- -h, --help: help instructions
- -b, --background: run the program as a background process (please don't run it more than once as it may create extra instances of this which will all be sending messages when the conditions are met and I'm sure you don't want multiple copies of the same message)
- -f, --front: run the program with the terminal active, this means that the program will output to the terminal. Functionally it's still the same.

Checklist:

Before running the program there are a few things to make sure are done to run the program smoothly:

- the program running in a virtual environment
- all the required libraries in their right versions are installed into the environment
- Twilio account is created. https://www.twilio.com/
- have at least one active number (can be seen under the "Active numbers" tab in the Twilio dashboard)
- have verified phone number(s). These are the phone numbers that will receive the messages, this is required as a way for Twilio to prevent abuse of their service for spam calls and messages. These can be seen under the "Verified Caller IDs" tab
- Have at least some money balance which can be seen at the top bar of the Twilio dashboard
- obtain both the Account SID and Auth Token which can be copied from the main Twilio dashboard

Syntax:

- py/python3/py3 main.py -mode "auth_token" "account_sid" "destination phone numbers in an array" "source phone number"

- auth_token:string
- account_sid:string
- destination phone numbers:list of strings (include the country code in each phone number)
- source phone number:string (include country code)


For a future update:
- Make headless mode to run on a .pyw version of the scraper

