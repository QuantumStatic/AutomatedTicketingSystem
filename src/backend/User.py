class User:
    def __init__(self, name:str, age:int, student:bool=False)):
        self.id = None
        self.age = age
        self.name = name
        self.student = student
    
    def _ticket_type(self) -> str:
        if self.student:
            return "Student"
        elif self.age < 12:
            return "Child"
        elif self.age > 65:
            return "Senior"
        else:
            return "Standard"


