import json
import mylog
import config
import pymysql

from gen_spec_vec import SpecVecGen
from db_config import *

from numpy import *

'''
DataGrip Init:
CREATE VIEW id_authors AS SELECT id, author_cn FROM journal_all_1_5
CREATE VIEW id_keywords AS SELECT id, keyword_cn FROM journal_all_1_5
'''


def dict_append(dict, key, element):
    if key not in dict:
        dict[key] = []
    dict[key].append(element)


def clustering(vecs):
    eps = 1e-9

    n = len(vecs)

    #divide the space, this part can be replaced by kmeans
    sp = []
    for i in range(100):
        sp.append([vecs[0][i], vecs[0][i]])
    for vec in vecs:
        for i in range(100):
            sp[i][0] = min(sp[i][0], vec[i])
            sp[i][1] = max(sp[i][1], vec[i])

    M = n / (log(n + 1) * 80)
    m = []
    for i in range(100):
        m.append((sp[i][1] - sp[i][0] + eps) / M)

    #grid records which element belongs to which part
    grid = {}
    for i in range(n):
        v = []
        for j in range(100):
            v.append((vecs[i][j] - sp[j][0] + eps) // m[j])
        dict_append(grid, tuple(v), i)
    k = len(grid)

    if k == 1:
        ret = []
        for i in range(n):
            ret.append(i)
        return [ret]

    #using cendroid of each part to clustering
    p = []
    for ps in grid.values():
        v = zeros(100)
        for pp in ps:
            v += vecs[pp]
        v *= [1 / len(ps)]
        p.append([v, ps])

    f = []
    for i in range(k):
        f.append(i)

    def find(x):
        if f[x] == x:
            return x
        f[x] = find(f[x])
        return f[x]

    def dis(u, v):
        puv = p[u][0] - p[v][0]
        return sqrt(dot(puv, puv))

    vis = zeros(k)

    rt = 0
    for i in range(k):
        if len(p[i][1]) > len(p[rt][1]):
            rt = i

    diss = []
    for i in range(k):
        if i != rt:
            diss.append(dis(rt, i))

    diss.sort()
    r0 = diss[int(floor(len(diss) * 0.73))]

    u = rt

    def getR(u):
        return r0 * len(p[u][1]) / len(p[rt][1])

    r = []
    for i in range(k):
        r.append(getR(i))

    while True:
        vis[u] = 1
        v = -1
        disv = 0
        for i in range(k):
            disi = dis(u, i)
            if disi < r[u] + eps:
                f[find(i)] = find(u)
            elif vis[i] == 0:
                if v == -1 or disv > disi:
                    v = i
                    disv = disi
        if v == -1:
            break
        if disv < r[u] + r[v] + eps:
            for i in range(k):
                if dis(v, i) < r[v] + r[i] + eps:
                    f[find(i)] = find(v)
        u = v

    ret = []
    for i in range(k):
        ret.append([])
    for i in range(k):
        ret[find(i)].append(i)

    #ans is a list of sublists, each sublist contains id of papers in the same cluster
    ans = []
    for it in ret:
        if len(it) == 0:
            continue
        vec = []
        for i in it:
            for j in p[i][1]:
                vec.append(j)
        vec.sort()
        ans.append(vec)
    return ans


if __name__ == '__main__':
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()

    author2papers = {}

    mylog.log.info('STARTED: Loading Model')
    spec_vec_gen = SpecVecGen(config.model_path)
    mylog.log.info('FINISHED: Loading Model')

    slt_paper = 'SELECT * FROM id_authors'
    mylog.log.info('STARTED: ' + slt_paper)
    cursor.execute(slt_paper)
    mylog.log.info('FINISHED: ' + slt_paper)

    mylog.log.info('STARTED: divide papers to authors')
    while True:
        paper = cursor.fetchone()
        if paper is None:
            break
        id = paper[0]
        author_cn = paper[1]
        authors = author_cn.split('||')
        for author in authors:
            if author == '':
                continue
            dict_append(author2papers, author, id)
    mylog.log.info('FINISHED: divide papers to authors')

    mylog.log.info('STARTED: Clustering')

    json_out = []

    cnt = 0
    for author, papers in author2papers.items():
        vecs = []
        for id in papers:
            slt_paper = 'SELECT keyword_cn FROM id_keywords WHERE id=\'' + id + '\''
            cursor.execute(slt_paper)
            keyword_cn = cursor.fetchone()[0]
            keywords = keyword_cn.split('||')
            vecs.append(array(spec_vec_gen.sentence2spec_vec(keywords)))
        #vecs are word2vec of papers, whose order is as same as the papers
        ret = clustering(vecs)
        element = [author, len(ret)]
        for cls in ret:
            vec = []
            for i in cls:
                vec.append(papers[i])
            element.append(vec)
        json_out.append(element)
        cnt += 1
        #solve first 100 authors
        if cnt == 100:
            break

    with open(config.output_path, "w", encoding='utf-8') as fd:
        json.dump(json_out, fd)

    mylog.log.info('FINISHED: Clustering')
