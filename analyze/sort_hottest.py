import json

def _sortCount(tar):
    return sorted(tar.items(), key = lambda tup:tup[1], reverse=True)

if __name__ == "__main__":
    data = None
    file_to_read = "result_person.json"
    with open(file_to_read, encoding="utf-8") as fd:
        data = json.load(fd)

    in_count = {}
    out_count = {}

    for line in data:
        in_city = line["to_pro"]
        out_city = line["from_pro"]
        if in_city == out_city:
            continue

        if not(in_city in in_count.keys()):
            in_count[in_city] = 0
        in_count[in_city] += 1

        if not(out_city in out_count.keys()):
            out_count[out_city] = 0
        out_count[out_city] += 1

    in_count = _sortCount(in_count)
    out_count = _sortCount(out_count)

    with open("in_rank.json", "w", encoding="utf-8") as fd:
        json.dump(in_count, fd, ensure_ascii=False)
    with open("out_rank.json", "w", encoding="utf-8") as fd:
        json.dump(out_count, fd, ensure_ascii=False)
    