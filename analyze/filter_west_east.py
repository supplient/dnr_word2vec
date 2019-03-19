import json
from Selector import Selector

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

if __name__ == "__main__":
    data = None
    file_to_read = "result_person.json"
    with open(file_to_read, encoding="utf-8") as fd:
        data = json.load(fd)

    selector = Selector(west_cities)
    (west2east, east2west) = selector.proData(data)

    with open("res_east2west.json", "w", encoding="utf-8") as fd:
        json.dump(east2west, fd, ensure_ascii=False)
    with open("res_west2east.json", "w", encoding="utf-8") as fd:
        json.dump(west2east, fd, ensure_ascii=False)
