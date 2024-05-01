class Recurring(Task):
    def __init__(self, _name, _start, _duration, _date, _type, _startDate, _endDate, _frequency):
        super.__init__(_name, _start, _duration, _date)
        self.type = _type
        self.startDate = _startDate
        self.endDate = _endDate
        self.frequency = _frequency