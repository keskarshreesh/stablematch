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

    def read_preferences(self):
        print("Enter resident preferences:")
        for i in range(1, self.num_residents + 1):
            line = input().strip().split(':')
            self.residents[int(line[0])] = [int(x) for x in line[1].split()]

        print("Enter hospital preferences and posts:")
        for i in range(1, self.num_hospitals + 1):
            line = input().strip().split(':')
            self.hospitals[int(line[0])]['posts'] = int(line[1])
            self.hospitals[int(line[0])]['prefs'] = [int(x) for x in line[2].split()]

    def gale_shapley_residents(self):
        # Simplified Gale-Shapley algorithm from residents' side
        free_residents = list(self.residents.keys())
        while free_residents:
            r = free_residents.pop(0)
            for h in self.residents[r]:
                if len(self.matches['hospitals'].get(h, [])) < self.hospitals[h]['posts']:
                    self.matches['hospitals'].setdefault(h, []).append(r)
                    self.matches['residents'][r] = h
                    break

    def gale_shapley_hospitals(self):
        # Simplified Gale-Shapley algorithm from hospitals' side
        for h, data in self.hospitals.items():
            for r in data['prefs']:
                if r not in self.matches['residents']:
                    if len(self.matches['hospitals'].get(h, [])) < data['posts']:
                        self.matches['hospitals'].setdefault(h, []).append(r)
                        self.matches['residents'][r] = h

    def display_matches(self):
        print("Resident-optimal matches:")
        for r, h in self.matches['residents'].items():
            print(f"Resident {r} is matched to Hospital {h}")

        print("Hospital-optimal matches:")
        for h, rs in self.matches['hospitals'].items():
            for r in rs:
                print(f"Hospital {h} is matched to Resident {r}")

# Example usage
try:
    n = int(input("Enter the number of residents: "))
    m = int(input("Enter the number of hospitals: "))
    match_system = StableMatch(n, m)
    match_system.read_preferences()
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
