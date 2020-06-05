from utility import *
from rhyme_metric import *


def cluster_level_nodes():
    content = read_file('vocab.txt')
    lines = content.split("\n")
    del content
    words = [l.split(' ')[0] for l in lines]
    del lines

    clusters = merge_nearest_words(words)
    json_write(clusters, 'hierarchical_clusters0.json')


def hierarchical_level(i):
    clusters_simple = json_read('hierarchical_clusters' + str(i) + '.json')

    clusters = []
    for cluster_words in clusters_simple:
        clusters.append({
            'words': cluster_words,
            'pattern': ''
        })

    pattern_set = {}
    for cluster in clusters:
        pattern = cluster['words'][0]
        for word in cluster['words'][1:]:
            pattern = rhyme_pattern(pattern, word)
        cluster['pattern'] = pattern
        if pattern in pattern_set:
            pattern_set[pattern].append(cluster['words'])
        else:
            pattern_set[pattern] = [cluster['words']]

    rep_patterns = [(p, pattern_set[p]) for p in pattern_set if len(pattern_set[p])>1]
    upper_level_clusters = merge_nearest_words([c['pattern'] for c in clusters])

    json_write(upper_level_clusters, 'hierarchical_clusters' + str(i+1) + '.json')


def merge_nearest_words(words):
    #clusters_file = open('hierarchical_clusters0.txt', 'a+')

    clusters = []
    remained_words = words.copy()
    clusters_num = 0
    for word1 in words:
        if not (word1 in remained_words):
            continue
        remained_words.remove(word1)
        cluster_words = []
        max_similarity = 0
        for word2 in remained_words:
            similarity = rhyme_similarity(word1, word2)
            if similarity > max_similarity:
                max_similarity = similarity
                cluster_words = [word2]
            elif (similarity == max_similarity) and (similarity > 0):
                cluster_words.append(word2)

        for w in cluster_words:
            remained_words.remove(w)

        cluster_words.append(word1)
        clusters.append(cluster_words)
        # clusters_file.write(', '.join(cluster_words) + "\n")
        clusters_num += 1

        if (clusters_num % 10) == 0:
            print("Cluster" + str(clusters_num) + ' Remained words:' + str(len(remained_words)))
            # clusters_file.flush()
        # print(cluster)

    #clusters_file.close()
    #json_write(remained_words, 'no_similars.json')
    return clusters


#cluster_level_nodes()
hierarchical_level(0)

