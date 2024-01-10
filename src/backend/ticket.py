from abc import ABC
import re

class Ticket(ABC):

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._type = "Generic"
        self._price = None
    
    @property
    def name(self):
        return self._type + " Ticket"

    def __str__(self):
        return self.name

    @property
    def price(self):
        return self._price

    @property
    def type(self):
        return self._type

    @classmethod
    def get_other_ticket_types(cls):
        return tuple(x() for x in Ticket.__subclasses__() if x != cls)


class StudentTicket(Ticket):
    def __init__(self):
        super().__init__()
        self._type = "Student"
        self._price = 5


class ChildTicket(Ticket):
    def __init__(self):
        super().__init__()
        self._type = "Child"
        self._price = 4


class SeniorTicket(Ticket):
    def __init__(self):
        super().__init__()
        self._type = "Senior"
        self._price = 3


class StandardTicket(Ticket):
    def __init__(self):
        super().__init__()
        self._type = "Standard"
        self._price = 10


def get_ticket_by_name(name: str) -> Ticket:
    """
    Returns:
        The state with the given name.
    """
    try:
        return eval(name+"Ticket")()
    except NameError:
        raise ValueError(f"No Ticket with name {name}") from NameError