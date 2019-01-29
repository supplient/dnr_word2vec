import os
cfp = os.path.dirname(os.path.realpath(__file__))
top_path = cfp
log_path = os.path.join(cfp, "log")
model_path = os.path.join(os.path.join(cfp, "model"), "word2vec.model")
output_path = os.path.join(os.path.join(cfp, "output"), "word.json")

origin_field = ["id", "source_url", "download_url", "title_cn", "title_en", "brief_cn", "brief_en", "classification_s", "doi_s", "author_cn", "author_en", "organization_each_cn", "organizations_simple_cn", "organization_detail_cn", "first_authors_cn", "journal_cn", "journal_en", "year_s", "issue_s", "keyword_cn", "keyword_en", "publication_date", "found_cn", "author_firstworkplace"]

per_progress = 1000

per_lines_corpus = 1000
max_lines_corpus = -1

size = 100
window = 10
min_count = 1
workers = 2
sg = 0 # CBOW
max_vocab_size = 20000000 # 20 million, 2GB