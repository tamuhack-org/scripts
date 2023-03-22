import os
from constants import director_data
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def sendText(number, message):
  client.messages.create(
    to=number, 
    from_=os.getenv('TWILIO_PHONE_NUMBER'),
    body=message)
  print("sent text to " + str(number))
  pass

copyString = input("Paste the copied string from tamuhack.com/slack:")
names = [name.strip() for name in copyString.lower().split("@")]
names[-1] = names[-1].split("get")[0].strip()

for name in names:
  if name in director_data:
    sendText(director_data[name], "Testing new TH script: COME TO 7:30 MEETING!")