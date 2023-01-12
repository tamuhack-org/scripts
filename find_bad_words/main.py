import json
from better_profanity import profanity

INPUT_FILENAME = "public_application_application_export_2023-01-11_185402.json"
OUTPUT_FILENAME = "output.txt"

applications = []
iteration = 1

with open(INPUT_FILENAME, encoding="utf-8") as input_file:
    try:
        applications = json.load(input_file)
    except json.JSONDecodeError:
        print("Make sure to remove the trailing comma from the json file")
        exit()
num_applications = len(applications)

with open(OUTPUT_FILENAME, "w") as output_file:
    for application in applications:
        print(f"{iteration}/{num_applications}")
        iteration += 1
        for field in application:

            entry = application[field]
            if not isinstance(entry, str):
                continue

            entry = entry.replace("'", " ")
            entry = entry.replace("\"", " ")

            if profanity.contains_profanity(entry):
                censored_str = profanity.censor(entry, "#")

                output_file.write(str(application["id"]) + "\n" + entry + "\n" + censored_str + "\n\n")
                break
                
print("\nDone!\nPlease review", OUTPUT_FILENAME)

