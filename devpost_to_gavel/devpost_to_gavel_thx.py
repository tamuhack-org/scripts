# Made by Naveen Iyer
# 9 June 2024

# ------ This script is for THX-style hackathons where IEEE manages the hardware tracks ------

# HOW TO USE
# ----------
# 1) Make a folder called "data" in the directory of this script
# 2) Create three text files inside the data folder containing each corresponding Devpost track name separated by line breaks
#    You can usually copy-paste this from Devpost
#    Put their filenames here
SOFTWARE_TRACKS_FILENAME = "tracks-software.txt"  # Software-only track names
HARDWARE_TRACKS_FILENAME = "tracks-hardware.txt"  # Hardware-only track names
GENERAL_TRACKS_FILENAME = "tracks-general.txt"  # Tracks that can be either software or hardware
# 3) Download the projects CSV from devpost
#    IMPORTANT: Run it through the "devpost_judging_attendance" script first to filter out projects that won't be judged
#    Then copy the output CSV to the "data" folder and put its filename here
PROJECTS_FILENAME = "devpost.csv"
# 4) Create an empty folder called "output" in the directory of this script 
# 5) Run the script!



import csv


def make_project_csv_row (project, include_tracks=False):
    if include_tracks:
        return [project["Project Title"], f"Table {project['__table_number']}", f"{project["Submission Url"]}\nTracks: {project["Opt-In Prizes"]}"]
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

with open(f"data/{GENERAL_TRACKS_FILENAME}") as in_file:
    for line in in_file.readlines():
        track_name = line.strip()
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


# Identify projects as software or hardware
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
        # print(f"WARNING: project {project['Project Title']} is NEITHER software nor hardware, ask the project members to specify one or the other")
        print(f"..........whatever: project {project['Project Title']} is NEITHER software nor hardware... i'll just lump them in with software")
        project["__is_software_project"] = True
print("")


# Assign each project a table number
table_number = 1
for project in projects:
    if project["__is_hardware_project"] and not (not project["__is_software_project"] and not project["__is_hardware_project"]) and not (project["__is_software_project"] and project["__is_hardware_project"]):
        project["__table_number"] = table_number
        print(f"Table {table_number}: {project['Project Title']} (hardware)")
        table_number += 1
# print(f"Software tables: 1-{table_number - 1}")
for project in projects:
    if project["__is_software_project"] or (not project["__is_software_project"] and not project["__is_hardware_project"]) or (project["__is_software_project"] and project["__is_hardware_project"]):
        project["__table_number"] = table_number
        print(f"Table {table_number}: {project['Project Title']} (software)")
        table_number += 1
# print(f"Hardware tables: {table_number}+")


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
            row = make_project_csv_row(project, include_tracks=True)
            if project["__is_software_project"]:
                software_writer.writerow(row)
            if project["__is_hardware_project"]:
                hardware_writer.writerow(row)


# Output table numbers
table_numbers_output_filename = "output/table_numbers.csv"
print(table_numbers_output_filename)
# sort projects by table number
projects.sort(key=lambda project: project["__table_number"])
with open(table_numbers_output_filename, "w") as out_file:
    writer = csv.writer(out_file)
    for project in projects:
        row = [project["Project Title"], project["__table_number"]]
        writer.writerow(row)


print("Everything should be in the \"output\" folder")
print("Make sure to tell hackers their table numbers (and make the spreadsheet look nicer!)")
print("All done!")

