#!/usr/bin/env python

import random
import csv

def main():
    # Configuration values
    total_residents = 100
    total_hospitals = 100
    resident_rol_len = 10  # Average length of resident preference list
    resident_rol_sd = 3  # Standard deviation of resident preference list length
    hospital_num_positions = 6  # Average number of positions per hospital
    hospital_num_positions_sd = 2  # Standard deviation of positions per hospital
    hospital_prefix = 'Hospital-'
    resident_prefix = 'Resident-'
    output_file = 'preferences.csv'

    # Initialize preference lists
    resident_prefs = [[] for _ in range(total_residents)]
    hospital_prefs = [[] for _ in range(total_hospitals)]

    # Generate resident preference lists
    for this_resident in range(total_residents):
        hospitals_randomized = list(range(total_hospitals))
        random.shuffle(hospitals_randomized)
        this_resident_rol_len = int(random.normalvariate(resident_rol_len, resident_rol_sd))
        resident_prefs[this_resident] = hospitals_randomized[:this_resident_rol_len]

    # Generate hospital preference lists and positions
    for this_hospital in range(total_hospitals):
        residents_applied = [i for i, prefs in enumerate(resident_prefs) if this_hospital in prefs]
        random.shuffle(residents_applied)
        hospital_prefs[this_hospital] = residents_applied
        positions = int(random.normalvariate(hospital_num_positions, hospital_num_positions_sd))
        hospital_prefs[this_hospital] = (positions, residents_applied)

    # Write output to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_residents, total_hospitals])  # First line: numbers of residents and hospitals
        
        # Write residents' preferences
        for index, prefs in enumerate(resident_prefs):
            row = [f"{resident_prefix}{index + 1}:"] + [f"{hospital_prefix}{h + 1}" for h in prefs]
            writer.writerow(row)
        
        # Write hospitals' preferences and posts
        for index, (positions, prefs) in enumerate(hospital_prefs):
            row = [f"{hospital_prefix}{index + 1}:{positions}:"] + [f"{resident_prefix}{r + 1}" for r in prefs]
            writer.writerow(row)

    print("Dataset generation complete.")

if __name__ == "__main__":
    main()
