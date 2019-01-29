from gensim.models import Word2Vec
from mylog import log
from corpus import Corpus

import config

def fetchLineWithSpecVec():
    log.info("Loading model...")
    model = Word2Vec.load(config.model_path)
    log.info("Load finished.")

    log.info("Initing corpus...")
    corpus = Corpus()
    log.info("Init finished.")

    count = 0
    for line in corpus.fetchLines(1):
        line = line[0]
        sentence = Corpus.line2sentence(line)
        spec_vec = None
        for word in sentence:
            if spec_vec is None:
                tmp = model.wv[word]
                spec_vec = [0.0 for x in range(len(tmp))]
                spec_vec += tmp
            else:
                spec_vec += model.wv[word]
        if spec_vec is None:
            raise Exception("spec_vec genearte failed for line:\n" + str(line))
        line["spec_vec"] = spec_vec.tolist()
        yield line

        count += 1
        if config.max_lines_corpus > 0:
            if count >= config.max_lines_corpus:
                break

if __name__ == "__main__":
    import json
    with open(config.output_path, "w") as fd:
        for line in fetchLineWithSpecVec():
            json.dump(line, fd)
            break