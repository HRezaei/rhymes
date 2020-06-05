


f = open('/home/hrezaei/codes/python/quran/Quran-en.maududi.txt')
c = f.read()
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

x = []
for sura in dic:
    x.append(' '.join(dic[sura]))

f = open('quranEnForGlove.txt', '+w')
f.writelines('\n'.join(x))
f.close()
