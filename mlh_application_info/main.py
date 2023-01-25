import json
import csv

APPLICATIONS_FILENAME = "public_application_application_export_2023-01-25_015159.json"
USERS_FILENAME = "public_user_user_export_2023-01-25_015912.json"
SCHOOLS_FILENAME = "schools.json"

OUTPUT_FILENAME = "output.csv"

applications = []
users = []
schools = []
iteration = 1

CLASSIFICATIONS = {
    "Fr": "Freshman",
    "So": "Sophomore",
    "Jr": "Junior",
    "Sr": "Senior",
    "Ma": "Master's Student",
    "PhD": "PhD Student",
    "O": "Other"
}

with open(APPLICATIONS_FILENAME, encoding="utf-8") as input_file:
    try:
        applications = json.load(input_file)
    except json.JSONDecodeError:
        print("Make sure to remove the trailing comma from the json file")
        exit()
num_applications = len(applications)

with open(USERS_FILENAME, encoding="utf-8") as input_file:
    try:
        users = json.load(input_file)
    except json.JSONDecodeError:
        print("Make sure to remove the trailing comma from the json file")
        exit()

with open(SCHOOLS_FILENAME, encoding="utf-8") as input_file:
    try:
        schools = json.load(input_file)
    except json.JSONDecodeError:
        print("Make sure to remove the trailing comma from the json file")
        exit()


with open(OUTPUT_FILENAME, "w", encoding="utf-8") as output_file:
    fieldnames = ["first_name", "last_name", "age", "email", "school", "level_of_study", "tamuhack_code_of_conduct", "mlh_code_of_conduct", "privacy_policy"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    # We do not collect ages from people so adults are listed as >=18 and minors as <18
    # We do not collect phone numbers
    # We do not collect country
    # We do not prompt for MLH Marketing Opt In

    for application in applications:
        print(f"{iteration}/{num_applications}")
        iteration += 1

        user_id = application["user_id"]
        user = None
        for u in users:
            if u["id"] == user_id:
                user = u
                break
        if user is None:
            print("applicant does not exist in users???")
            exit()
        
        school_id = application["school_id"]
        school = None
        if school_id == 2074:
            school = application["school_other"]
        else:
            for s in schools:
                if s["pk"] == school_id:
                    school = s["fields"]["name"]
                    break
            if school is None:
                print("applicant's school does not exist in schools???")
                exit()

        applicant = {
            "first_name": application["first_name"],
            "last_name": application["last_name"],
            "age": ">=18" if application["is_adult"] else "<18",
            "email": user["email"],
            "school": school,
            "level_of_study": CLASSIFICATIONS[application["classification"]],
            "tamuhack_code_of_conduct": "checked",
            "mlh_code_of_conduct": "checked",
            "privacy_policy": "checked"
        }
        writer.writerow(applicant)
                
print("\nDone!\nSaved to", OUTPUT_FILENAME)

