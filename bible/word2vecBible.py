

import json
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

def build_model():
    fp = open("BibleForWord2Vec.json", "r")
    bible = json.load(fp)

    print(len(bible))

    model = Word2Vec(bible, size=50, window=15, min_count=1, workers=4)
    model.save("word2vec.model")


def write_vectors():
    model = Word2Vec.load("word2vec.model")

    lines = []
    for key in model.wv.index2word:
        lines.append(key + ' ' + ' '.join(['{:.6f}'.format(f) for f in model.wv[key].tolist()]))

    fp = open('w2vectors.txt', '+w')
    fp.write("\r\n".join(lines))
    fp.close()


#build_model()
write_vectors()