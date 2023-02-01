import json
import random

#Get the json file for the raffle
INPUT_FILENAME = "./volunteer_workshopevent.json"
scans = []

with open(INPUT_FILENAME, encoding="utf-8") as input_file:
    try:
        scans = json.load(input_file)
    except json.JSONDecodeError:
        print("Make sure to remove the trailing comma from the json file")
        exit()
num_users = len(scans)
#get a random number between 0 and the number of users
winner = scans[random.randint(0, num_users - 1)]

#The winning user id is printed. You'll have to crossreference this with the users table to get the winner.
print(winner)
