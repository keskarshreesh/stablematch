class NameTable:
    def __init__(self, size):
        self.size = size
        self.names = []
        self.name_to_index = {}
        self.index_to_name = {}

    def add(self, name):
        if name not in self.name_to_index:
            if len(self.names) < self.size:
                self.names.append(name)
                index = len(self.names)  # index is 1-based
                self.name_to_index[name] = index
                self.index_to_name[index] = name
            else:
                raise Exception("Table overflow")
        else:
            raise Exception("Name already exists")

    def look_up_by_name(self, name):
        return self.name_to_index.get(name, 0)

    def look_up_by_index(self, index):
        return self.index_to_name.get(index, None)

    def table_size(self):
        return len(self.names)

    def get_max_name_length(self):
        return max(len(name) for name in self.names) if self.names else 0

    def set_required_posn(self, index, posn):
        if index <= len(self.names):
            self.index_to_name[posn] = self.index_to_name.pop(index)

    def set_all_required_posns(self):
        # This method would reorder all names to match some external positional requirement.
        # Example usage might not be straightforward without context, so it's simplified here.
        pass

    def get_true_entry(self, posn):
        # This method is meant to return the original index of an entry based on a required position
        # Without the specifics of the original usage, this will just return the entry at posn
        return self.index_to_name.get(posn, None)


# Example of using the NameTable class
try:
    table = NameTable(10)
    table.add("Alice")
    table.add("Bob")
    print("Index of Alice:", table.look_up_by_name("Alice"))
    print("Name at index 2:", table.look_up_by_index(2))
    print("Max name length:", table.get_max_name_length())
except Exception as e:
    print(e)
