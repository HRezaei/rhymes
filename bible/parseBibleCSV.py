
csv_file = open('bsb.csv')
content = csv_file.read()
lines = content.split('\n')
lines_splitted = [k.split('@') for k in lines]
#v = [b[2] for b in l if len(b)>2]
dic = {}
for line in lines_splitted:
    if len(line) != 2 :
        print(line)
        continue
    book_chapter_verseNum, verse = line
    book_chapter, verse_num = book_chapter_verseNum.split(':')
    if len(verse) < 3:
        print(verse)
        continue

    if book_chapter in dic:
        dic[book_chapter].append(verse)
    else:
        dic[book_chapter] = [verse]


def write_for_glove():
    x = []
    for chapter in dic:
        x.append(' '.join(dic[chapter]))

    path = 'BibleForGlove.txt'
    f = open(path, '+w')
    f.writelines('\n'.join(x))
    f.close()
    print('Written in ' + path)


def write_for_word2vec():
    import json
    from nltk.tokenize import word_tokenize
    x = []
    for chapter in dic:
        for verse in dic[chapter]:
            x.append(word_tokenize(verse))

    f = open('BibleForWord2Vec.json', '+w', encoding='utf8')
    json.dump(x, f, ensure_ascii=False)
    f.close()


write_for_word2vec()
