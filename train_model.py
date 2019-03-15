from gensim.models import Word2Vec
from mylog import log
from corpus import Corpus

import config


# 将关键词看做一个句子，使用CBOW法训练Word2Vec，然后将每篇文章的关键词的词向量加起来，作为该文章的特征向量
if __name__ == "__main__":
    # init database
    log.info("Initing corpus...")
    corpus = Corpus()
    log.info("Initing finished.")

    # configure modle
    model = Word2Vec(
        size=config.size,
        window=config.window,
        min_count=config.min_count,
        workers=config.workers,
        sg=config.sg,
        max_vocab_size=config.max_vocab_size)

    # start training
    count = 0
    big_count = 0
    log.info("Start training...")
    if config.max_lines_corpus > 0:
        log.info("Only " + str(config.max_lines_corpus) + " lines of corpus can be used.")
    else:
        log.info("No line limit for corpus.")
    for sentences in corpus.fetchSentences(config.per_lines_corpus):
        # build vocab
        if count==0:
            model.build_vocab(sentences, update=False)
        else:
            model.build_vocab(sentences, update=True)
        # train
        model.train(sentences, total_examples=len(sentences), epochs=model.epochs)

        count = count + len(sentences)
        tmp = int(count / config.per_progress)
        if tmp > big_count:
            big_count = tmp
            log.info("Trained " + str(count) + " lines...")
    log.info("Training finished, used " + str(count) + " lines of corpus.")

    # save model
    log.info("Saving model...")
    model.save(config.model_path)
    log.info("Saved.")