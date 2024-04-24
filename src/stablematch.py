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
            num_residents, num_hospitals = map(int, first_row[0].split())
            
            # Initialize residents and hospitals if not already set (optional)
            self.num_residents = num_residents
            self.num_hospitals = num_hospitals
            self.residents = {i: [] for i in range(1, num_residents + 1)}
            self.hospitals = {i: {'posts': 0, 'prefs': []} for i in range(1, num_hospitals + 1)}
            
            # Read residents' preferences
            for _ in range(num_residents):
                row = next(reader)
                resident_id, hospitals = row[0].split(':')
                self.residents[int(resident_id)] = [int(h) for h in hospitals.split(',')]

            # Read hospitals' preferences and posts
            for _ in range(num_hospitals):
                row = next(reader)
                hospital_id, posts, prefs = row[0].split(':')
                self.hospitals[int(hospital_id)]['posts'] = int(posts)
                self.hospitals[int(hospital_id)]['prefs'] = [int(r) for r in prefs.split(',')]

    def gale_shapley_residents(self):
        # Same as before
        free_residents = list(self.residents.keys())
        while free_residents:
            r = free_residents.pop(0)
            for h in self.residents[r]:
                if len(self.matches['hospitals'].get(h, [])) < self.hospitals[h]['posts']:
                    self.matches['hospitals'].setdefault(h, []).append(r)
                    self.matches['residents'][r] = h
                    break

    def gale_shapley_hospitals(self):
        # Same as before
        for h, data in self.hospitals.items():
            for r in data['prefs']:
                if r not in self.matches['residents']:
                    if len(self.matches['hospitals'].get(h, [])) < data['posts']:
                        self.matches['hospitals'].setdefault(h, []).append(r)
                        self.matches['residents'][r] = h

    def display_matches(self):
        # Same as before
        print("Resident-optimal matches:")
        for r, h in self.matches['residents'].items():
            print(f"Resident {r} is matched to Hospital {h}")
        print("Hospital-optimal matches:")
        for h, rs in self.matches['hospitals'].items():
            for r in rs:
                print(f"Hospital {h} is matched to Resident {r}")

# Example usage
try:
    match_system = StableMatch(0, 0)  # Initialize with zero and let CSV dictate sizes
    match_system.read_preferences_from_csv('preferences.csv')
    match_system.gale_shapley_residents()
    print("After Residents' Proposals:")
    match_system.display_matches()
    match_system.gale_shapley_hospitals()
    print("After Hospitals' Proposals:")
    match_system.display_matches()
except TableOverflowError as e:
    print(e)
except Exception as e:
    print("An error occurred:", e)
