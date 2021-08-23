from genericpath import isfile
import os
from pathlib import Path
from word_clustering import VectorClustering
from loguru import logger

def list_datasets():
    datasets = [item for item in os.listdir('input') if os.path.isdir('input/' + item)]
    return datasets

def check_dataset_validity(dataset_path):
    sentences_path = dataset_path + '/raw.txt'
    if not isfile(sentences_path):
        print("Could not find: " + sentences_path)
        return False
    return True

def make_output_folders(dataset_name):
    output_path = 'output/' + dataset_name  
    clusters_path = output_path + '/clusters'
    Path(clusters_path).mkdir(parents=True, exist_ok=True)

    vectors_path = output_path + '/vectors'
    Path(vectors_path).mkdir(parents=True, exist_ok=True)

    Path(output_path + '/reports').mkdir(parents=True, exist_ok=True)

    #make also a folder in input:
    Path('input/' + dataset_name + '/vectors').mkdir(parents=True, exist_ok=True)


datasets = list_datasets()

logger.info('Found ' + str(len(datasets)) + ' datasets in input folder')
default_embeddings = [
    'WordToVec',
    #'Glove'
]

for dataset in datasets:
    logger.info('Processing dataset: ' + dataset)
    try: 
        #check if corpus exists:
        if not check_dataset_validity('input/' + dataset):
            print("Skipped " + dataset)
            continue

        #create folders, if not properly structured:
        make_output_folders(dataset)

        experiment = VectorClustering(dataset)
        for embedding_system in default_embeddings:
            experiment.perform_clustering(embedding_system)
            experiment.calculate_inter_similarity(embedding_system)
    except Exception as e:
        logger.error(e)