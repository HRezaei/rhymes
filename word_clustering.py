from preprocessor import Preprocessor
from sklearn.cluster import KMeans
from numbers import Number
from pandas import DataFrame
import numpy as np
import os, sys, codecs, argparse, pprint, time
from utils import *
#from word_arithmetic import *
from cluster_comparison import assess_clusters
from loguru import logger
import importlib


class VectorClustering():
	def __init__(self, dataset_name, num_clusters=1000, num_jobs=-1) -> None:
		self.dataset_name = dataset_name
		self.input_path = 'input/' + dataset_name
		self.output_path = 'output/' + dataset_name
		self.num_clusters = num_clusters
		self.num_jobs = num_jobs
		self.reports_path = self.output_path + '/reports'

	def vector_file_path(self, embedding_system):
		file_path = self.input_path + '/vectors/' + embedding_system + '.txt'
		if os.path.isfile(file_path):
			return file_path
		
		prepared = self.generate_vectors(embedding_system, file_path)
		if prepared:
			return file_path

	def clusters_file_path(self, embedding_system):
		return self.output_path + '/clusters/' + embedding_system + '.json'

	def find_word_clusters(self, labels_array, cluster_labels):
		cluster_to_words = autovivify_list()
		for c, i in enumerate(cluster_labels):
			cluster_to_words[i].append(labels_array[c])
		return cluster_to_words

	def perform_clustering(self, embedding_system):
		
		cluster_to_words = None
		start_time = time.time()
		num_words = sys.maxsize
		clusters_file_path = self.clusters_file_path(embedding_system)

		logger.info("Loading vectors: " + embedding_system)
		df, labels_array = build_word_vector_matrix(self.vector_file_path(embedding_system), num_words)
		logger.info("Loaded vectors: " + embedding_system)

		logger.info("Started clustering: " + embedding_system)
		kmeans_model = KMeans(init='k-means++', n_clusters=self.num_clusters, n_jobs=self.num_jobs, n_init=10)
		kmeans_model.fit(df)
		logger.info("Finished clustering: " + embedding_system)

		cluster_labels   = kmeans_model.labels_
		# cluster_inertia = kmeans_model.inertia_
		cluster_to_words = list(self.find_word_clusters(labels_array, cluster_labels).values())

		# cache these clustering results
		logger.info('Saving clusters for later use')
		save_json(clusters_file_path, cluster_to_words)
		logger.info('Saved {} clusters to {}.'.format(len(cluster_to_words), clusters_file_path))

		# if this kmeans fitting has already been cached
		if start_time != None:
			logger.info("--- {:.2f} seconds ---".format((time.time() - start_time)))

	def calculate_inter_similarity(self, embedding_system):
		clusters = load_json(self.clusters_file_path(embedding_system))
		logger.info("Measuring rhytmic similarity within clusters...")
		plot = assess_clusters(clusters)
		plot.suptitle('Rhytmic Similarity Distribution Over ' + embedding_system.capitalize() + ' Vectors\nDataset: ' + self.dataset_name.upper())
		logger.info("Finished")
		plot.savefig(self.reports_path + '/' + embedding_system + '.jpg')
		plot.show()
	
	def generate_vectors(self, embedding_system, vectors_file_path):
		logger.debug('Looking for the module for class: ' + embedding_system)
		embedding_module = importlib.find_loader(embedding_system)
		if embedding_module is None:
			raise Exception('No module is implemented for embedding: ' + embedding_system)
		logger.debug('Found module in: ' + embedding_module.path)

		logger.debug('Importing module: ' + embedding_system)
		embedding_module = importlib.import_module(embedding_system)
		logger.debug('Imported.')


		embedding_class = getattr(embedding_module, embedding_system)

		embedding_instance = embedding_class(self.dataset_name)
		embedding_instance.generate_vectors(vectors_file_path)
		return True

if __name__ == '__main__':
	embedding_system = 'glove'
	clusters = VectorClustering('cnn')
	#clusters.perform_clustering(embedding_system)
	clusters.interSimilarity(embedding_system)