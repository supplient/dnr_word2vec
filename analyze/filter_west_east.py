import json

west_cities = {
    "四川",
    "云南",
    "贵州",
    "西藏",
    "重庆",
    "陕西",
    "甘肃",
    "青海",
    "新疆",
    "宁夏",
    "内蒙古",
    "广西"
}

def isEastCity(target):
    for city_name in west_cities:
        if city_name in target:
            return False
    return True

def checkLine(line):
    from_east = isEastCity(line["from_pro"])
    to_east = isEastCity(line["to_pro"])
    if from_east and not to_east:
        # east to west
        return 1
    elif not from_east and to_east:
        # west to east
        return 2
    else:
        return 0

def proData(data):
    east2west = []
    west2east = []
    
    for line in data:
        flag = checkLine(line)
        if flag == 1:
            east2west.append(line)
        elif flag == 2:
            west2east.append(line)
    
    return (east2west, west2east)

if __name__ == "__main__":
    data = None
    file_to_read = "result_person.json"
    with open(file_to_read, encoding="utf-8") as fd:
        data = json.load(fd)

    (east2west, west2east) = proData(data)

    with open("res_east2west.json", "w", encoding="utf-8") as fd:
        json.dump(east2west, fd, ensure_ascii=False)
    with open("res_west2east.json", "w", encoding="utf-8") as fd:
        json.dump(west2east, fd, ensure_ascii=False)
