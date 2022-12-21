#Matthew Sanders
#Scrapes raid pokemon data from thesilphroad.com and sends an email with the data
#Last edited 12/21/22
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import time
from selenium import webdriver
from selenium.webdriver import Chrome

print("Enter API key: ")
API_key = input()
print("Enter client ID key: ")
clientID = input()
print("Enter client secret: ")
clientSecret = input()

"""
difficulty levels and their associated hex colors
dif0 = impossible
dif1 = hardcore
dif2 = hard
dif3 = medium
dif4 = easy
dif5 = very easy
dif6 = trivial
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

def gmail_send_message(creds, text):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(text)

        print("Enter email to send to: ")
        recipient = input()
        message['To'] = recipient
        message['From'] = 'gduser2@workspacesamples.dev'
        message['Subject'] = 'Weekly Raid Bosses'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()
        
        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

"""Shows basic usage of the Gmail API.
Lists the user's Gmail labels.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()

except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f'An error occurred: {error}')

#create driver
website = "https://thesilphroad.com/raid-bosses"
path = r"C:\Users\18506\Downloads\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(path)
driver.get(website)

#collect data
raidBosses = []

#Raid boss name
names = driver.find_elements("xpath", "//div[@class='boss-name']")
i = 0
for name in names:
    raidBosses.append([0 for x in range(4)])
    raidBosses[i][0] = name.text
    i += 1

#Type of pokemon
#Knowing the type of pokemon you are fighting will help you choose your team to confront it
i = 0
allPokeTypes = driver.find_elements("xpath", "//div[@class='type-icons']")
for x in allPokeTypes:
    indivTypes = x.find_elements("xpath", "img")
    k = 0
    for y in indivTypes:
        #strips the image src to get the type
        delSubStrings = y.get_attribute("src").replace("https://assets.thesilphroad.com/img/pogo-assets/type-", "").replace(".png", "")
        raidBosses[i][k+1] = delSubStrings
        k += 1
    if raidBosses[i][2] == 0:
        raidBosses[i][2] = "none"
    i += 1

#Recommended group size to beat the boss
#Dark colors indicate a more difficult boss with a certain size group, lighter colors indicate an easier boss with a certain size group
#The same boss can be impossible to beat on your own, but easy to beat with a group of ten people
#Find recommended group size by searching through list until the diffculty is medium or easier
i = 0
#All web elements that are identified by the class hexagons. This class contains color that identifies how hard it is to beat
allPokemonDiffs = driver.find_elements("xpath", "//div[@class='hexagons']")
for x in allPokemonDiffs:
    indivDiffs = x.find_elements("xpath", "div")
    diffs = []
    for y in indivDiffs:
        diffNum = y.get_attribute("class").replace("hexagon difficulty", "")
        diffs.append(diffNum)
    recommendGroupSize = 0
    while int(diffs[recommendGroupSize]) < 3:
        recommendGroupSize += 1
    raidBosses[i][3] = recommendGroupSize + 1
    i += 1

#send to email
message = "" 
i = 0
while i < len(raidBosses):
    message += raidBosses[i][0] + "\n"
    message += "Type 1: " + raidBosses[i][1] + "\nType 2: " + raidBosses[i][2] + "\n"
    message += "Recommended Group Size: " + str(raidBosses[i][3]) + "\n"
    message += '\n'
    i += 1

gmail_send_message(creds, message)

while True:
    pass

