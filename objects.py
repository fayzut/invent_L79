class good():
    def __init__(self, name, invent_number):
        self.name = name
        self.inv_num = invent_number
        self.comments = ''
        self.is_on_balance = True
        self.status = 'h'
        Тип - ид_тип_имущества
        Подтип - ид_подтип_имущества

    Местонахождение - ид_место
    Ответственный - ид_ответственного
    !!! Часть
    комплекта: ид_комплекта - не
    реализовано
    Дата
    приобретения
    Время
    эксплуатации(через
    сколько
    можно
    списывать)