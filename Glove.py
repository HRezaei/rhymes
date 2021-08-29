import os
import utils
import nltk
from loguru import logger
from pathlib import Path

class Glove():
    def __init__(self, dataset_name) -> None:
        input_file_path = 'input/' + dataset_name + '/raw.txt'
        if not os.path.isfile(input_file_path):
            raise Exception('Could not find ' + input_file_path)

        self.input_file_path = input_file_path
        self.dataset_path = 'input/' + dataset_name 
        self.corpus_file_path = self.dataset_path + '/corpus_for_glove.txt'
        if not os.path.isfile('lib/glove/build/glove'):
            self.setup_glove()

    def setup_glove(self):
        os.system('cd lib && git clone https://github.com/stanfordnlp/glove && cd glove && make')
        os.system('chmod +x lib/glove-for-rhymes.sh')
 
    def generate_vectors(self, vectors_file_path):
        if not os.path.isfile(self.corpus_file_path):
            self.__generate_corpus_file()
        
        self.write_vectors(vectors_file_path)

    def __generate_corpus_file(self):
        logger.info('Reading corpus file and preprocessing')
        lines = utils.read_file(self.input_file_path).split("\n")
        last_document_lines = []
        documents = []
        for line in lines:
            if not line.strip():
                document = " ".join(last_document_lines)
                documents.append(document)
                last_document_lines = []
                continue
            words = [word.lower() for word in nltk.word_tokenize(line) if word.isalpha()]    
            last_document_lines.append(" ".join(words))
        if len(last_document_lines):
            document = " ".join(last_document_lines)
            documents.append(document)
        utils.write_file(self.corpus_file_path, "\n\n".join(documents)) 
        logger.info('Finished. Saving sentences for later use in Glove')
        return True

    def write_vectors(self, vectors_file_path):

        input_dir = os.path.realpath(self.dataset_path)
        output_dir = os.path.realpath(os.path.dirname(vectors_file_path))
        script_path = 'cd lib && ./glove-for-rhymes.sh ' + input_dir + ' ' + output_dir 
        
        os.system(script_path)
        
