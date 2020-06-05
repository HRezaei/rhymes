

import json
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

'''fp = open("quranForWord2Vec.json", "r")
quran = json.load(fp)

print(len(quran))

model = Word2Vec(quran, size=50, window=15, min_count=1, workers=4)
model.save("word2vec.model")
'''

model = Word2Vec.load("word2vec.model")

lines = []
for key in model.wv.index2word:
    lines.append(key + ' ' + ' '.join(['{:.6f}'.format(f) for f in model.wv[key].tolist()]))

fp = open('w2vectors.txt', '+w')
fp.write("\r\n".join(lines))
fp.close()

