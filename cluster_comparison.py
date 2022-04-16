from rhyme_metric import rhyme_similarity
from utils import *
import matplotlib.pyplot as plt
from itertools import chain
from random import random
    

def cluster_rhyme_similarity(words):
    sim = 0
    total = len(words)
    for i in range(0, total):
        for j in range(i+1, total):
            sim = sim + rhyme_similarity(words[i], words[j])
    return sim / ((total * (total-1))/2)


def clusters_average_rhyme_similarity(clusters):
    similarities = []
    for c in clusters:
        if len(c) < 2:
            # similarities.append(0)
            continue
        similarities.append(100 * cluster_rhyme_similarity(c))

    average = sum(similarities) / len(similarities)
    return average, similarities


def assess_clusters(clusters):
    avg, data = clusters_average_rhyme_similarity(clusters)
    print("Clusters avg:", avg)
    max_similarity = max(data)
    charts_data = [data]

    random_clusters = {}
    all_words = list(chain.from_iterable(clusters))
    for w in all_words:
        toss = int(random() * 1000)
        if toss in random_clusters:
            random_clusters[toss].append(w)
        else:
            random_clusters[toss] = [w]

    avg, data = clusters_average_rhyme_similarity(list(random_clusters.values()))
    max_similarity = int(max(max_similarity, max(data)))
    charts_data.append(data)
    colors = ['#0072AE', '#FD7E10']
    bin_width = 1
    fig, axes = plt.subplots(2, sharex=True, sharey=False)
    for ax, data, color in zip(axes.flatten(), charts_data, colors):
        ax.hist(data, bins=range(0, max_similarity+bin_width, bin_width), log=True, color=color)

    plt.xlabel("Average rhythmic similarity (percentage)", fontsize=12)
    plt.ylabel("Number of clusters", fontsize=12)
    #print("Max sim: ", max_similarity)
    print("Random Clusters avg:", avg)
    return plt
    #sorted_stats = {k: str(v) + " " + ", ".join(clusters[k]) for k, v in sorted(cluster_stats.items(), key=lambda item: item[1])}
    #return sorted_stats


def compare_clusters(clusters1, clusters2):
    pairs1 = []
    for cluster in clusters1:
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                if cluster[i] < cluster[j]:
                    pairs1.append((cluster[i], cluster[j]))
                else:
                    pairs1.append((cluster[j], cluster[i]))

    print("clusters1 pairs: " + str(len(pairs1)))
    matches = 0
    for cluster in clusters2:
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                if cluster[i] < cluster[j]:
                    pair = (cluster[i], cluster[j])
                else:
                    pair = (cluster[j], cluster[i])
                if pair in pairs1:
                    matches += 1
                    print(matches)
    return matches


def read_clusters(path):
    '''
    Reads a text file, each line representing a cluster, each line a comma separated list of words
    :param path: string path to file
    :return: array of clusters
    '''
    content = read_file(path)
    lines = content.split("\n")
    clusters = [[word.strip() for word in line.split(",") if len(word.strip())] for line in lines]
    return clusters




