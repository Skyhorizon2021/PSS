class Transient(Task):
    def __init__(self, _name, _start, _duration, _date, _type):
        super.__init__(_name, _start, _duration, _date)
        self.type = _type
