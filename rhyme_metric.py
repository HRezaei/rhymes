from utils import load_json


def rhyme_similarity(word1, word2):
    """cache_key = word1+'@'+word2 if word1 > word2 else word2+'@'+word1
    if cache_key in rhyme_similarity.cache:
        return rhyme_similarity.cache[cache_key]
    """
    len1 = len(word1)
    len2 = len(word2)
    min_len = min(len1, len2)
    sim = 0
    for i in range(0, min_len):
        if word1[-i-1] == word2[-i-1] or (word1[-i-1] == '_') or (word2[-i-1] == '_'):
            sim = sim + 1
    similarity = sim / (len1 + len2 - min_len)
    #rhyme_similarity.cache[cache_key] = similarity
    return similarity


rhyme_similarity.cache = {}  # json_read('similarities_cache.json')


def rhyme_pattern(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    min_len = min(len1, len2)
    sim = 0
    pattern = ''
    for i in range(0, min_len):
        if word1[len1-i-1] == word2[len2-i-1]:
            pattern = word1[len1-i-1] + pattern
        else :
            pattern = '_' + pattern

    for i in range(max(len1, len2) - min_len):
        pattern = '_' + pattern
    return pattern
