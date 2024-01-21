# Made by Naveen Iyer
# 20 January 2024
# For TAMUhack 2024

# HOW TO USE
# ----------
# 1) Make a folder called "data" in the directory of this script
# 2) Create a text file inside the data folder containing each Devpost track name separated by line breaks
#    You can usually copy-paste this from Devpost
#    Put its filename here
SOFTWARE_TRACKS_FILENAME = "tracks-software-howdyhack-2023.txt"
HARDWARE_TRACKS_FILENAME = "tracks-hardware-howdyhack-2023.txt"
# 3) Download the projects CSV from devpost
#    Put its filename here
PROJECTS_FILENAME = "projects-howdyhack-2023.csv"
# 4) Create an empty folder called "output" in the directory of this script 
# 5) Run the script!



import csv


def make_project_csv_row (project):
    return [project["Project Title"], f"Table {project['__table_number']}", project["Submission Url"]]

def sanitize_filename (filename):
    return filename.replace(':', '-').replace(' ', '_').replace("/", "-")


# Read and store tracks
tracks = set()
software_tracks = set()
hardware_tracks = set()
with open(f"data/{SOFTWARE_TRACKS_FILENAME}") as in_file:
    for line in in_file.readlines():
        track_name = line.strip()
        software_tracks.add(track_name)
        tracks.add(track_name)

with open(f"data/{HARDWARE_TRACKS_FILENAME}") as in_file:
    for line in in_file.readlines():
        track_name = line.strip()
        hardware_tracks.add(track_name)
        tracks.add(track_name)


# Read projects CSV file
projects = []
num_drafts = 0
with open(f"data/{PROJECTS_FILENAME}") as in_file:
    reader = csv.DictReader(in_file)
    for row in reader:
        # Exclude draft projects and projects hidden by admins
        if row["Project Status"] != "Draft" and "(Hidden)" not in row["Project Status"]:
            projects.append(row)
print("number of projects:", len(projects))
print("number of drafts:", num_drafts, "\n")


# Identify projects that are software or hardware
for project in projects:
    project_tracks = project["Opt-In Prizes"].strip().split(", ")
    project["__is_software_project"] = False
    project["__is_hardware_project"] = False
    is_software_project = False
    is_hardware_project = False
    for track in project_tracks:
        if track in software_tracks:
            is_software_project = True
            project["__is_software_project"] = True
        if track in hardware_tracks:
            is_hardware_project = True
            project["__is_hardware_project"] = True
    
    if is_software_project and is_hardware_project:
        print(f"WARNING: project {project['Project Title']} is BOTH software and hardware, ask the project members to specify one or the other")
    if not is_software_project and not is_hardware_project:
        print(f"WARNING: project {project['Project Title']} is NEITHER software nor hardware, ask the project members to specify one or the other")
print("")


# Assign each project a table number
software_table_number = 1
hardware_table_number = 1
for project in projects:
    if project["__is_software_project"] or (not project["__is_software_project"] and not project["__is_hardware_project"]):
        project["__table_number"] = f"S{software_table_number}"
        software_table_number += 1
    if project["__is_hardware_project"]:
        project["__table_number"] = f"H{hardware_table_number}"
        hardware_table_number += 1


# Write output files for each track
for track_name in tracks:
    track_output_filename = f"output/{sanitize_filename(track_name)}_gavel.csv"
    print(track_output_filename)
    with open(track_output_filename, "w") as out_file:
        writer = csv.writer(out_file)
        for project in projects:
            project_tracks = project["Opt-In Prizes"].split(", ")
            if track_name in project_tracks:
                row = make_project_csv_row(project)
                writer.writerow(row)

overall_software_output_filename = "output/best_overall_software_gavel.csv"
overall_hardware_output_filename = "output/best_overall_hardware_gavel.csv"
print(overall_software_output_filename)
print(overall_hardware_output_filename, "\n")
with open(overall_software_output_filename, "w") as software_out_file:
    with open(overall_hardware_output_filename, "w") as hardware_out_file:
        software_writer = csv.writer(software_out_file)
        hardware_writer = csv.writer(hardware_out_file)
        for project in projects:
            row = make_project_csv_row(project)
            if project["__is_software_project"]:
                software_writer.writerow(row)
            if project["__is_hardware_project"]:
                hardware_writer.writerow(row)


# Output table numbers
table_numbers_output_filename = "output/table_numbers.csv"
print(table_numbers_output_filename)
with open(table_numbers_output_filename, "w") as out_file:
        writer = csv.writer(out_file)
        for project in projects:
            if project["__is_software_project"]:
                row = [project["Project Title"], project["__table_number"]]
                writer.writerow(row)
        for project in projects:
            if project["__is_hardware_project"]:
                row = [project["Project Title"], project["__table_number"]]
                writer.writerow(row)


print("\nEverything should be in the \"output\" folder")
print("Make sure to tell hackers their table numbers (and make the spreadsheet look nicer!)")
print("All done!")

