from gensim.models import Word2Vec
from mylog import log
from corpus import Corpus

import config

class SpecVecGen:
    def __init__(self, model_path):
        '''
        @param
            model_path: the path of Word2Vec's path, like "model/word2vec.model"
        '''
        self.model = Word2Vec.load(model_path)

    def sentence2spec_vec(self, sentence):
        spec_vec = None
        for word in sentence:
            if spec_vec is None:
                tmp = self.model.wv[word]
                spec_vec = [0.0 for x in range(len(tmp))]
                spec_vec += tmp
            else:
                spec_vec += self.model.wv[word]
        if spec_vec is None:
            raise Exception("spec_vec genearte failed for sentence:\n" + str(sentence))
        return spec_vec.tolist()

    def int_genSpecVec(self, line):
        sentence = Corpus.line2sentence(line)
        return self.sentence2spec_vec(sentence)

    def genSpecVec(self, origin_line):
        '''Calculate spec_vec for a line.
        @param
            origin_line: an origin line fetched from database, like ("asngy033", "zzy", "bhuv", ...).
        @return
            The spec_vec for the line, in the format like [0.3, 0.1, -3.2, ...].
            The dim is determined by Word2Vec's model.
        '''
        line = Corpus.addFieldForSingle(origin_line)
        return self.int_genSpecVec(line)

if __name__ == "__main__":
    log.info("Loading model...")
    spec_vec_gen = SpecVecGen(config.model_path)
    log.info("Load finished.")

    log.info("Initing corpus...")
    corpus = Corpus()
    log.info("Init finished.")

    import json
    with open(config.output_path, "w") as fd:
        count = 0
        for origin_line in corpus.fetchOriginLines(1):
            spec_vec = spec_vec_gen.genSpecVec(origin_line[0])
            json.dump(spec_vec, fd)
            break

            count += 1
            if config.max_lines_corpus > 0:
                if count >= config.max_lines_corpus:
                    break