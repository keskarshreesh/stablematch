class Name:
    MAX_LENGTH = 20

    def __init__(self, name=""):
        if len(name) > self.MAX_LENGTH:
            self.name = name[:self.MAX_LENGTH]
            self.overflow = True
        else:
            self.name = name
            self.overflow = False
        self.success = bool(name)

    @classmethod
    def blank_name(cls):
        return cls()

    @staticmethod
    def get_name(input_string):
        """
        Simulate reading a name from input.
        Trims input to the first space or end of the input.
        """
        trimmed_name = input_string.strip().split()[0] if input_string.strip() else ""
        if len(trimmed_name) > Name.MAX_LENGTH:
            trimmed_name = trimmed_name[:Name.MAX_LENGTH]
            overflow = True
        else:
            overflow = False
        success = bool(trimmed_name)
        name = Name(trimmed_name)
        name.overflow = overflow
        name.success = success
        return name

    def put_name(self):
        """
        Simulates writing a name to standard output.
        """
        print(self.name)

    def name_to_string(self):
        return self.name

    def length(self):
        return len(self.name)

    def __gt__(self, other):
        """
        Overrides the '>' operator for lexicographical comparison.
        """
        return self.name > other.name

# Example usage
name1 = Name.get_name("Alice Smith")
name2 = Name.get_name("Bob")
name3 = Name.blank_name()

print("Name1:", name1.name_to_string(), "Length:", name1.length(), "Overflow:", name1.overflow)
print("Name2:", name2.name_to_string(), "Length:", name2.length(), "Overflow:", name2.overflow)
print("Name3 (Blank):", name3.name_to_string(), "Length:", name3.length())

# Comparison
print("Is Name1 > Name2?", name1 > name2)

# Display name
name1.put_name()
name2.put_name()
