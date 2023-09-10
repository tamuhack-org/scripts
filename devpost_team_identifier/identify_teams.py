# Team Identifier Script (for TAMUhack 2022 and beyond)
# Naveen Iyer

import json
import csv
import re

print("-- TAMUhack Team Identifier Script --")

DEVPOST_PROJECTS_CSV_FILENAME = "projects-howdyhack-2023.csv"

def sanitize_and_load_json (file_name):
    """Reads a JSON file, fixes unpleasant formatting, and returns a JSON object"""
    with open(file_name, encoding="utf-8") as file:
        contents = file.read()

        # FIXME this gets confused by double backslash in the JSON export
        # TODO this whole script is crap. rewrite using CSV DictWriter LOL

        # For some reason, when you export the database data as JSON,
        # escape sequences are exported fine "\n" but backslashes are not escaped "\".
        # The following takes care of that
        contents = re.sub(r"\\[^bfnrtv'\"\\](?!\\)", "\\\\\\\\", contents)

        # Also my FOSS database viewer exports JSON with a trailing comma like a weirdo
        contents = re.sub(r"},\s*]", "}]", contents)

        return json.loads(contents)


# Read in application and user data
print("Parsing application JSON...")
applications = {}
for application in sanitize_and_load_json("obos_application_application.json"):
    applications[application["user_id"]] = application

print("Parsing user JSON...")
users = {}
for user in sanitize_and_load_json("obos_user_user.json"):
    users[user["id"]] = user

for user_id in applications:
    if user_id in users:
        applications[user_id]["email"] = users[user_id]["email"]
    else:
        applications.pop(user_id)


# Read in devpost submission data
print("Parsing devpost CSV...")
submissions = []
with open(DEVPOST_PROJECTS_CSV_FILENAME, encoding="utf-8") as file:
    with open(DEVPOST_PROJECTS_CSV_FILENAME, encoding="utf-8") as file2:
        reader = csv.DictReader(file)
        row_reader = csv.reader(file2)

        # ignore header row
        for this_row_list in row_reader:
            break

        for row in reader:
            
            # HACK this sucks
            row_list = []
            for this_row_list in row_reader:
                row_list = this_row_list
                break
                
            # Skip the title row and skip teams without a submission
            if row["Submission Url"] == "":
                continue

            submission = {
                "title": row["Project Title"],
                "url": row["Submission Url"],
                "categories": row["Opt-In Prizes"].split(", "),
                "members": [
                    {
                        "firstName": row["Submitter First Name"],
                        "lastName": row["Submitter Last Name"],
                        "email": row["Submitter Email"],
                        "foundStatus": "",
                        "checkedinStatus": ""
                    }
                ]
            }

            for i in range(19, 19 + (3 * int(row["Additional Team Member Count"])), 3):
                # print(row_list[19])
                submission["members"].append({
                        "firstName": row_list[i],
                        "lastName": row_list[i + 1],
                        "email": row_list[i + 2],
                        "foundStatus": "",
                        "checkedinStatus": ""
                    })

            submissions.append(submission)


# See if team members appear in application data
members_not_found = []
members_not_checked_in = []
print("Matching devpost data with application data...")
for submission in submissions:
    for member in submission["members"]:
        member_application = None
        for application in applications.values():  # See if emails appear
            if member["email"].lower() == application["email"].lower():
                member_application = application
                break
        if member_application is None:
            for application in applications.values():  # See if full names appear
                if member["firstName"].lower() == application["first_name"].lower() and member["lastName"].lower() == application["last_name"].lower():
                    member_application = application
                    break
        if member_application is None:
            member["foundStatus"] = "Not found in application data"
            members_not_found.append(member)
        
        # Report if members are not "confirmed" or "checked in"
        if member_application is not None:
            # if not (member_application["status"] == "C" or member_application["status"] == "I"):
            if not (member_application["status"] == "I"):
                member["checkedinStatus"] = "Undesirable status: " + member_application["status"]
                members_not_checked_in.append(member)


# Output a csv file
print("Creating output CSV file...")
with open("team_info.csv", "w", encoding="utf-8", newline="") as out_file:
    writer = csv.writer(out_file)

    for submission in submissions:
        writer.writerow([submission["title"], submission["url"]])
        for i in range(0, max(len(submission["categories"]), len(submission["members"]))):
            row = [""]

            # List categories
            if i < len(submission["categories"]):
                row.append(submission["categories"][i])
            else:
                row.append("")
            row.append("")

            # List members
            if i < len(submission["members"]):
                member = submission["members"][i]
                member_info = [member["firstName"], member["lastName"], member["email"], member["foundStatus"], member["checkedinStatus"]]
                row += member_info

            writer.writerow(row)
        
        writer.writerow([])
        writer.writerow([])



print("Done!\nOutput data in team_info.csv")

print("\n\n\nThe following team members were not found in the application data!")
for member in members_not_found:
    print(f"{member['firstName']} {member['lastName']} - {member['email']}")

print("\n\n\nThe following team members never checked in at the event!")
for member in members_not_checked_in:
    print(f"{member['firstName']} {member['lastName']} - {member['email']}")

print("\n\n")
print(members_not_found[0])
print(members_not_found[1])
