import os
cfp = os.path.dirname(os.path.realpath(__file__))
top_path = cfp
log_path = os.path.join(cfp, "log")
model_path = os.path.join(os.path.join(cfp, "model"), "word2vec.model")
output_path = os.path.join(os.path.join(cfp, "output"), "word.json")

origin_field = ["keyword_cn"]

per_progress = 1000

per_lines_corpus = 1000
max_lines_corpus = -1

size = 100
window = 10
min_count = 1
workers = 2
sg = 0 # CBOW
max_vocab_size = 20000000 # 20 million, 2GB