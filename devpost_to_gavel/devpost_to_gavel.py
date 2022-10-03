# Made by Naveen Iyer
# 30 September 2022
# For HowdyHack 2022

# HOW TO USE
# ----------
# 1) Make a folder called "data" in the directory of this script
# 2) Create a text file inside the data folder containing each Devpost track name separated by line breaks
#    You can usually copy-paste this from Devpost
#    Put its filename here
TRACKS_FILENAME = "tracks-tamuhack-2022.txt"
# 3) Download the projects CSV from devpost
#    Put its filename here
PROJECTS_FILENAME = "projects-howdy-hack-2022.csv"
# 4) Create an empty folder called "output" in the directory of this script 
# 5) Run the script!



import csv


def make_project_csv_row (project):
    return [project["Project Title"], f"Table {project['__table_number']}", project["Submission Url"]]


# Read and store tracks
tracks = set()
with open(f"data/{TRACKS_FILENAME}") as in_file:
    for line in in_file.readlines():
        tracks.add(line.strip())

# Read projects CSV file
projects = []
with open(f"data/{PROJECTS_FILENAME}") as in_file:
    reader = csv.DictReader(in_file)
    for row in reader:
        # Exclude draft projects and projects hidden by admins
        if row["Project Status"] != "Draft" and "(Hidden)" not in row["Project Status"]:
            projects.append(row)

# Assign each project a table number
for num in range(len(projects)):
    projects[num]["__table_number"] = num + 1

# Write output files for each track including arbitrary "all-projects" track
for track_name in tracks:
    with open(f"output/{track_name.replace(':', '_')}_gavel.csv", "w") as out_file:
        writer = csv.writer(out_file)
        for project in projects:
            project_tracks = project["Opt-In Prizes"].split(", ")
            if track_name in project_tracks:
                row = make_project_csv_row(project)
                writer.writerow(row)

with open(f"output/all_projects_gavel.csv", "w") as out_file:
        writer = csv.writer(out_file)
        for project in projects:
            row = make_project_csv_row(project)
            writer.writerow(row)

# Output table numbers
with open(f"output/table_numbers.csv", "w") as out_file:
        writer = csv.writer(out_file)
        for project in projects:
            row = [project["Project Title"], project["__table_number"]]
            writer.writerow(row)


print("Output stuff in \"output\" folder")
print("Make sure to tell hackers their table numbers (and make the spreadsheet look nicer!)")
print("All done!")

