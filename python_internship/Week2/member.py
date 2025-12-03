class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def display_info(self):
        """Polymorphism: same method name as Book.display_info"""
        print(f"Member -> Name: {self.name}, ID: {self.member_id}")
