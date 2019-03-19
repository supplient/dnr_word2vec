import json
from Selector import GroupSelector

group_cities = {
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

    selector = GroupSelector(group_cities)
    (in2in, in2out) = selector.proData(data)

    with open("res_in2in.json", "w", encoding="utf-8") as fd:
        json.dump(in2in, fd, ensure_ascii=False)
    with open("res_in2out.json", "w", encoding="utf-8") as fd:
        json.dump(in2out, fd, ensure_ascii=False)
