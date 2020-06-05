from utility import *
from random import random
from rhyme_metric import rhyme_similarity


def basic_clustering():
    content = read_file('vocab.txt')
    lines = content.split("\n")
    words = [l.split(' ')[0] for l in lines]
    vocab_size = len(words)

    clusters = []
    chosen = []
    while len(clusters) < 1000:
        tos = int(random() * vocab_size)
        if tos in chosen:
            continue
        chosen.append(tos)
        clusters.append({
            'centroid': words[tos],
            'words': []
        })

    clusters = change_centroids(clusters, words)
    json_write(clusters, 'basic_clusters1.json')


def change_centroids(clusters, words):
    word_index = 0
    for word in words:
        word_index += 1
        max_similarity = 0
        selected_cluster = 0
        for cluster_index in range(1000):
            cluster = clusters[cluster_index]
            similarity = rhyme_similarity(cluster['centroid'], word)
            if similarity > max_similarity:
                max_similarity = similarity
                selected_cluster = cluster_index
        if (word_index % 1000) == 0:
            print('Processed ' + str(word_index))
        clusters[selected_cluster]['words'].append(word)

    changes = 0;
    for cluster_index in range(1000):
        cluster = clusters[cluster_index]
        max_similarity = 0
        for word in cluster['words']:
            similarities = 0
            for word2 in cluster['words']:
                if word2 == word:
                    continue
                similarities = similarities + rhyme_similarity(word, word2)
            if similarities > max_similarity:
                max_similarity = similarities
                new_centroid = word
        if new_centroid != cluster['centroid']:
            cluster['centroid'] = new_centroid
            changes += 1
    print(changes)
    return clusters


def refine_clusters(num):
    content = read_file('vocab.txt')
    lines = content.split("\n")
    words = [l.split(' ')[0] for l in lines]

    clusters = json_read('basic_clusters' + str(num) + '.json')
    for cluster in clusters:
        cluster['words'] = []
    clusters = change_centroids(clusters, words)
    json_write(clusters, 'basic_clusters' + str(num + 1) + '.json')


#basic_clustering()
refine_clusters(4)
#json_write(rhyme_similarity.cache, 'similarities_cache.json')