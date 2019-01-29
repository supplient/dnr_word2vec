from mylog import log
from readBasicData import readBasicData

import config

def addField(db_data):
    res = []
    for d in db_data:
        line_res = {}
        field = config.origin_field
        if len(field) != len(d):
            raise Exception("field number: " + str(len(field)) + " != line of data number: " + str(len(d)))
        for i in range(len(field)):
            line_res[field[i]] = d[i]
        res.append(line_res)
    return res

def keywords2sentence(keywords):
    return keywords.split("||")

class Corpus:
    @classmethod
    def line2sentence(cls, line):
        keywords = line["keyword_cn"]
        return keywords2sentence(keywords)

    def __init__(self):
        self.db = readBasicData()
        self.db.search()

    def fetchLines(self, size):
        res = self.db.readManyData(size)
        while not res is None:
            yield addField(res)
            res = self.db.readManyData(size)

    def fetchSentences(self, size):
        count = 0
        max_flag = False
        for origin in self.fetchLines(size):
            sentences = []
            for line in origin:
                sentence = Corpus.line2sentence(line)
                sentences.append(sentence)

                count = count + 1
                if config.max_lines_corpus > 0:
                    if count >= config.max_lines_corpus:
                        max_flag = True
                        break
            yield sentences
            if max_flag:
                break