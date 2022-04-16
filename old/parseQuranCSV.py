


f = open('Arabic-Original.csv')
c = f.read()[1:]
l = c.split('\n')
lp = [k.split('|') for k in l]
v = [b[2] for b in lp if len(b)>2]
dic = {}
for aye in lp:
    sura = aye[0]
    if len(aye)<3:
        print(aye)
        continue
    sura = int(sura)
    if sura in dic:
        dic[sura].append(aye[2])
    else:
        dic[sura] = [aye[2]]


def writeForGlove():
    x = []
    for sura in dic:
        x.append(' '.join(dic[sura]))

    f = open('quranForGlove.txt', '+w')
    f.writelines('\n'.join(x))
    f.close()
    print(v[1:20])


def writeAsRawForBoth():
    x = []
    for sura in dic:
        x.append('\n'.join(dic[sura]))
        x.append("\n")
    f = open('../input/quran/raw.txt', '+w')
    f.writelines('\n'.join(x))
    f.close()
    print(v[1:20])


def writeForWord2Vec():
    import json
    from nltk.tokenize import word_tokenize
    x = []
    for sura in dic:
        for aye in dic[sura]:
            x.append(word_tokenize(aye))

    f = open('quranForWord2Vec.json', '+w', encoding='utf8')
    json.dump(x, f, ensure_ascii=False)
    f.close()


if __name__ == '__main__':
    #writeForWord2Vec()
    #writeForGlove()
    writeAsRawForBoth()
