import csv

class TableOverflowError(Exception):
    """Exception raised when the number of entries does not match expected counts."""
    pass

class StableMatch:
    def __init__(self, num_residents, num_hospitals):
        self.num_residents = num_residents
        self.num_hospitals = num_hospitals
        self.residents = {i: [] for i in range(1, num_residents + 1)}
        self.hospitals = {i: {'posts': 0, 'prefs': []} for i in range(1, num_hospitals + 1)}
        self.matches = {'residents': {}, 'hospitals': {}}

    def read_preferences_from_csv(self, preferences_csv):
        with open(preferences_csv, 'r') as file:
            reader = csv.reader(file)
            first_row = next(reader)
            num_residents, num_hospitals = map(int, first_row)
            # Initialize residents and hospitals if not already set (optional)
            self.num_residents = num_residents
            self.num_hospitals = num_hospitals
            self.residents = {i: [] for i in range(1, num_residents + 1)}
            self.hospitals = {i: {'posts': 0, 'prefs': []} for i in range(1, num_hospitals + 1)}
            
            # Read residents' preferences
            for _ in range(num_residents):
                row = next(reader)
                resident_id = int(row[0].split('-')[1])
                hospitals = row[1:]
                self.residents[int(resident_id)] = [int(h.split('-')[1]) for h in hospitals]

            # Read hospitals' preferences and posts
            for _ in range(num_hospitals):
                row = next(reader)
                hospital, posts = row[0].split(':')
                hospital_id = hospital.split('-')[1]
                prefs = row[1:]
                self.hospitals[int(hospital_id)]['posts'] = int(posts)
                self.hospitals[int(hospital_id)]['prefs'] = [int(r.split('-')[1]) for r in prefs]

    def gale_shapley_residents(self):
        free_residents = list(self.residents.keys())
        while free_residents:
            r = free_residents.pop(0)
            for h in self.residents[r]:
                if len(self.matches['hospitals'].get(h, [])) < self.hospitals[h]['posts']:
                    self.matches['hospitals'].setdefault(h, []).append(r)
                    self.matches['residents'][r] = h
                    break

    def gale_shapley_hospitals(self):
        for h, data in self.hospitals.items():
            for r in data['prefs']:
                if r not in self.matches['residents']:
                    if len(self.matches['hospitals'].get(h, [])) < data['posts']:
                        self.matches['hospitals'].setdefault(h, []).append(r)
                        self.matches['residents'][r] = h

    def display_resident_optimal_matches(self):
        print("Resident-optimal matches by resident:")
        for r, h in self.matches['residents'].items():
            print(f"Resident {r} is matched to Hospital {h}")

    def display_hospital_optimal_matches(self):
        print("Hospital-optimal matches by Hospital:")
        for h in sorted(self.hospitals.keys()):
            residents = self.matches['hospitals'].get(h, [])
            residents_display = ', '.join(f"Resident {r}" for r in residents)
            print(f"Hospital {h}: {residents_display}")
    
    def percentage_unmatched_residents(self):
        unmatched = [r for r in self.residents if r not in self.matches['residents']]
        return (len(unmatched)/self.num_residents)*100

    def percentage_underfilled_hospitals(self):
        underfilled = [h for h, details in self.hospitals.items() 
                       if len(self.matches['hospitals'].get(h, [])) < details['posts']]
        return (len(underfilled)/self.num_hospitals)*100
    
    def percentage_top_k_preferences_residents(self, k):
        matched_in_top_k = 0
        for r, h in self.matches['residents'].items():
            if r in self.residents and h in self.residents[r][:k]:
                matched_in_top_k += 1
        total_matched_residents = len(self.matches['residents'])
        if total_matched_residents == 0:
            return 0  # Avoid division by zero
        return (matched_in_top_k / total_matched_residents) * 100
    
    def average_percentage_top_k_prefs_per_hospital(self, k):
        hospital_match_quality = {}
        for h, matched_residents in self.matches['hospitals'].items():
            top_k_matched = 0
            total_matched = len(matched_residents)
            if total_matched == 0:
                hospital_match_quality[h] = 0
            else:
                top_k_residents = self.hospitals[h]['prefs'][:min(k, len(self.hospitals[h]['prefs']))]
                for r in matched_residents:
                    if r in top_k_residents:
                        top_k_matched += 1
                hospital_match_quality[h] = (top_k_matched / total_matched) * 100
        
        if not hospital_match_quality:  # if the dictionary is empty
            return 0  # No matches happened
        # Calculate the average percentage across all hospitals
        return sum(hospital_match_quality.values()) / len(hospital_match_quality)

    def display_match_summary(self):
        # Calculate and display the summary of the matching process
        num_unmatched_residents = self.percentage_unmatched_residents()
        num_underfilled_hospitals = self.percentage_underfilled_hospitals()
        top_k_resident_matches = self.percentage_top_k_preferences_residents(3)
        top_k_hospital_matches = self.average_percentage_top_k_prefs_per_hospital(3)
        print(f"Number of unmatched residents: {num_unmatched_residents}")
        print(f"Number of underfilled hospitals: {num_underfilled_hospitals}")
        print(f"Top k matches for residents: {top_k_resident_matches}")
        print(f"Top k matches for hospitals: {top_k_hospital_matches}")

match_system = StableMatch(0, 0)
match_system.read_preferences_from_csv('../data/preferences.csv')
match_system.gale_shapley_residents()
print("After Residents' Proposals:")
match_system.display_resident_optimal_matches()
match_system.display_match_summary()

match_system = StableMatch(0, 0)
match_system.read_preferences_from_csv('../data/preferences.csv')
match_system.gale_shapley_hospitals()
print("After Hospitals' Proposals:")
match_system.display_hospital_optimal_matches()
match_system.display_match_summary()
