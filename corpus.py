from mylog import log
from readBasicData import readBasicData

import config

class Corpus:
    @classmethod
    def addFieldForSingle(cls, d):
        line_res = {}
        field = config.origin_field
        if len(field) != len(d):
            raise Exception("field number: " + str(len(field)) + " != line of data number: " + str(len(d)))
        for i in range(len(field)):
            line_res[field[i]] = d[i]
        return line_res

    @classmethod
    def addFieldForMulti(cls, db_data):
        res = []
        for d in db_data:
            line_res = Corpus.addFieldForSingle(d)
            res.append(line_res)
        return res

    @classmethod
    def keywords2sentence(cls, keywords):
        return keywords.split("||")

    @classmethod
    def line2sentence(cls, line):
        keywords = line["keyword_cn"]
        return Corpus.keywords2sentence(keywords)

    def __init__(self):
        self.db = readBasicData()
        self.db.search()

    def fetchOriginLines(self, size):
        res = self.db.readManyData(size)
        while not res is None:
            yield res
            res = self.db.readManyData(size)

    def fetchLines(self, size):
        res = self.db.readManyData(size)
        while not res is None:
            yield Corpus.addFieldForMulti(res)
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