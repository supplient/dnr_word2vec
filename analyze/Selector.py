from abc import ABCMeta, abstractmethod
def _getYear(s):
    year_str = s[0:4]
    return int(year_str)

class InternalSelector:
    __metaclass__ = ABCMeta

    def __init__(self, in_cities):
        self.in_cities = in_cities

    def isInCity(self, target):
        for city_name in self.in_cities:
            if city_name in target:
                return True
        return False

    @abstractmethod
    def checkLine(self, line):
        pass

    def proData(self, data):
        in2out = {}
        out2in = {}
    
        for line in data:
            flag = self.checkLine(line)
            year = _getYear(line["to_time"]) # TODO Concern about whether from_time or to_time
            to_list = None
            if flag == 1:
                to_list = in2out
            elif flag == 2:
                to_list = out2in
            else:
                continue
            
            if not(year in to_list.keys()):
                to_list[year] = []
            to_list[year].append(line)
    
        return (in2out, out2in)

class Selector(InternalSelector):
    def __init__(self, in_cities):
        InternalSelector.__init__(self, in_cities)

    def checkLine(self, line):
        from_in = InternalSelector.isInCity(self, line["from_pro"])
        to_in = InternalSelector.isInCity(self, line["to_pro"])
        if from_in and not to_in:
            # in to out
            return 1
        elif not from_in and to_in:
            # out to in
            return 2
        else:
            return 0

class GroupSelector(InternalSelector):
    def __init__(self, in_cities):
        InternalSelector.__init__(self, in_cities)

    def checkLine(self, line):
        from_in = InternalSelector.isInCity(self, line["from_pro"])
        to_in = InternalSelector.isInCity(self, line["to_pro"])
        if from_in and to_in:
            # in to in
            return 1
        elif (not from_in and to_in) or (from_in and not to_in):
            # out to in || in to out
            return 2
        else:
            return 0
