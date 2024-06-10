# Made by Naveen Iyer
# 9 June 2024


ATTENDANCE_FORM_RESPONSES_CSV_FILENAME = "attendance_form_responses.csv"  # Exported from the Google Forms responses spreadsheet
DEVPOST_PROJECTS_FILENAME = "devpost.csv"  # Exported from devpost
OUTPUT_FILENAME = "output.csv"

import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

present_urls = {}
with open(ATTENDANCE_FORM_RESPONSES_CSV_FILENAME) as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        if row[0] == "Timestamp":
            continue
        if row[2] == "Yes!":
            present_urls[row[1].strip()] = False

projects = []
num_submissions = 0
print("Fetching project URLs from devpost...")
with open(DEVPOST_PROJECTS_FILENAME) as in_file:
    reader = csv.DictReader(in_file)
    for row in tqdm(reader):
        num_submissions += 1
        submission_url = row["Submission Url"]

        req = requests.get(submission_url)
        soup = BeautifulSoup(req.text, "lxml")
        software_url = soup.find("meta", property="og:url")
        if software_url is None:
            continue
        software_url = software_url["content"]

        if software_url in present_urls:
            projects.append(row)
            present_urls[software_url] = True

with open(OUTPUT_FILENAME, "w") as out_file:
    writer = csv.DictWriter(out_file, fieldnames=projects[0].keys())
    writer.writeheader()
    for project in projects:
        writer.writerow(project)

print("WARNING: The following projects were marked as present in the attendance form but were not found in the devpost CSV")
for url, found in present_urls.items():
    if not found:
        print(url)

print(f"\n{len(projects)}/{num_submissions} teams responded that they will be present during judging.")
print(f"Their data has been saved to {OUTPUT_FILENAME}")







