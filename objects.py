from datetime import date


class Object:
    def __init__(self, name):
        self.id = 0
        self.name = name


class Responsible(Object):
    def __init__(self, fio, office_id=0):
        super().__init__(fio)
        self.office_id = office_id


class Type(Object):
    def __init__(self, name):
        super().__init__(name)


class Status(Object):
    def __init__(self, name):
        super().__init__(name)


class SubType(Type):
    def __init__(self, name, parent_type):
        super().__init__(name)
        self.parent_type = parent_type


class LocationType(Type):
    def __init__(self, name):
        super().__init__(name)


class Location(Object):
    def __init__(self, name):
        super().__init__(name)
        self.type = ""


class Good(Object):
    def __init__(self, name, invent_number):
        super().__init__(name)
        self.inv_num = invent_number
        self.comments = ''
        self.is_on_balance = True
        self.status = Status("status")
        self.type = Type("Type")
        self.subtype = SubType("SubType", self.type)
        self.location = Location("Location")
        self.responsible = Responsible("Responsible")
        self.bought_date = date.today()  # 01/06/2010
        # !!! Часть
        # комплекта: ид_комплекта - не реализовано
        self.can_be_used = 0
