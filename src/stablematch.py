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

    def get_match_summary(self):
        # Calculate and display the summary of the matching process
        k_vals = [1,3,5,7,9]
        summary_dict = {
            "percentage_unmatched_residents": self.percentage_unmatched_residents(),
            "percentage_underfilled_hospitals": self.percentage_underfilled_hospitals(),
        }
        
        for k in k_vals:
            summary_dict[f"top_{k}_resident_matches"] = self.percentage_top_k_preferences_residents(k)
            summary_dict[f"top_{k}_hospital_matches"] = self.average_percentage_top_k_prefs_per_hospital(k)
        
        return summary_dict

def run_exp_1():
    dataset_root = "../data/exp_1"
    num_residents = 500
    num_hospitals = 140
    summary_dict_resident_side_match = {
        "percentage_unmatched_residents": [],
        "percentage_underfilled_hospitals": [],
        "top_1_resident_matches": [],
        "top_1_hospital_matches": [],
        "top_3_resident_matches": [],
        "top_3_hospital_matches": [],
        "top_5_resident_matches": [],
        "top_5_hospital_matches": [],
        "top_7_resident_matches": [],
        "top_7_hospital_matches": [],
        "top_9_resident_matches": [],
        "top_9_hospital_matches": [],
    }
    summary_dict_hospital_side_match = {
        "percentage_unmatched_residents": [],
        "percentage_underfilled_hospitals": [],
        "top_1_resident_matches": [],
        "top_1_hospital_matches": [],
        "top_3_resident_matches": [],
        "top_3_hospital_matches": [],
        "top_5_resident_matches": [],
        "top_5_hospital_matches": [],
        "top_7_resident_matches": [],
        "top_7_hospital_matches": [],
        "top_9_resident_matches": [],
        "top_9_hospital_matches": [],
    }
    for file_num in range(1,6):
        match_system = StableMatch(0, 0)
        match_system.read_preferences_from_csv(f"{dataset_root}/r_{num_residents}_h_{num_hospitals}/preferences_{file_num}.csv")
        match_system.gale_shapley_residents()
        # match_system.display_resident_optimal_matches()
        current_file_summary = match_system.get_match_summary()
        for metric in current_file_summary:
            summary_dict_resident_side_match[metric].append(current_file_summary[metric])

        match_system = StableMatch(0, 0)
        match_system.read_preferences_from_csv(f"{dataset_root}/r_{num_residents}_h_{num_hospitals}/preferences_{file_num}.csv")
        match_system.gale_shapley_hospitals()
        # match_system.display_hospital_optimal_matches()
        current_file_summary = match_system.get_match_summary()
        for metric in current_file_summary:
            summary_dict_hospital_side_match[metric].append(current_file_summary[metric])
    
    print("After Residents' Proposals:")
    for metric in summary_dict_resident_side_match:
        metric_avg = 0
        for metric_val in summary_dict_resident_side_match[metric]:
            metric_avg += metric_val
        metric_avg /= len(summary_dict_resident_side_match[metric])
        print(f"{metric}: {metric_avg}")
    
    print("After Hospitals' Proposals:")
    for metric in summary_dict_hospital_side_match:
        metric_avg = 0
        for metric_val in summary_dict_hospital_side_match[metric]:
            metric_avg += metric_val
        metric_avg /= len(summary_dict_hospital_side_match[metric])
        print(f"{metric}: {metric_avg}")

if __name__ == "__main__":
    run_exp_1()