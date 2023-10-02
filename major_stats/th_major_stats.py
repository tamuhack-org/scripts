
# Naveen Iyer
# 27 July 2023

import csv

INPUT_CSV_FILENAME = "th23.csv"
NUM_MAJORS_TO_PRINT = 100
ONLY_CHECKED_IN = True

majors = {}

with open(INPUT_CSV_FILENAME, encoding="utf-8") as input_file:
    reader = csv.DictReader(input_file)

    for row in reader:
        if row["status"] != "I":
            continue

        major = row["major"].lower()
        if major in majors:
            majors[major] += 1
        else:
            majors[major] = 1

majors_list = list(majors.items())
majors_list.sort(key=lambda x: -x[1])

for major in majors_list[:NUM_MAJORS_TO_PRINT]:
    print(f"{major[0]}: {major[1]}")
