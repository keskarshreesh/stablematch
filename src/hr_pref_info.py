class PrefInfo:
    def __init__(self, num_residents, num_hospitals):
        self.num_residents = num_residents
        self.num_hospitals = num_hospitals
        self.residents = [Resident() for _ in range(num_residents + 1)]
        self.hospitals = [Hospital() for _ in range(num_hospitals + 1)]

class Resident:
    def __init__(self):
        self.pref_list = []
        self.rank = {}
        self.assigned = False

class Hospital:
    def __init__(self):
        self.pref_list = []
        self.rank = {}
        self.posts_filled = 0
        self.num_posts = 0
        self.last_assignee = 0

def get_pref_info(pref_info, resident_inputs, hospital_inputs):
    for i, line in enumerate(resident_inputs):
        parts = line.split(':')
        prefs = parts[1].strip().split()
        pref_info.residents[i + 1].pref_list = [int(x) for x in prefs]
        for rank, hosp in enumerate(pref_info.residents[i + 1].pref_list):
            pref_info.residents[i + 1].rank[hosp] = rank

    for i, line in enumerate(hospital_inputs):
        parts = line.split(':')
        num_posts = int(parts[1].strip())
        prefs = parts[2].strip().split()
        hospital = pref_info.hospitals[i + 1]
        hospital.num_posts = num_posts
        hospital.pref_list = [int(x) for x in prefs]
        for rank, res in enumerate(hospital.pref_list):
            hospital.rank[res] = rank

def gs_algorithm_residents(pref_info):
    free_residents = [i for i in range(1, pref_info.num_residents + 1) if not pref_info.residents[i].assigned]
    while free_residents:
        resident = free_residents.pop(0)
        for hospital_id in pref_info.residents[resident].pref_list:
            hospital = pref_info.hospitals[hospital_id]
            if hospital.posts_filled < hospital.num_posts:
                hospital.posts_filled += 1
                hospital.last_assignee = resident
                pref_info.residents[resident].assigned = True
                break
            else:
                # Handling case where hospital is full but current proposal is better than the last assignee
                last_assignee = hospital.last_assignee
                if hospital.rank[resident] < hospital.rank[last_assignee]:
                    free_residents.append(last_assignee)
                    hospital.last_assignee = resident
                    pref_info.residents[last_assignee].assigned = False
                    pref_info.residents[resident].assigned = True
                    break
        if not pref_info.residents[resident].assigned:
            free_residents.append(resident)

# Example of setting up the problem
num_residents = 3
num_hospitals = 3
resident_inputs = [
    "1 : 2 3 1",
    "2 : 1 2 3",
    "3 : 3 1 2"
]
hospital_inputs = [
    "1 : 2 : 1 2 3",
    "2 : 1 : 2 3 1",
    "3 : 1 : 3 2 1"
]

pref_info = PrefInfo(num_residents, num_hospitals)
get_pref_info(pref_info, resident_inputs, hospital_inputs)
gs_algorithm_residents(pref_info)
