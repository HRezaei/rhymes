import os
import utils
import nltk
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from loguru import logger


class WordToVec():
    def __init__(self, dataset_name) -> None:
        input_file_path = 'input/' + dataset_name + '/raw.txt'
        if not os.path.isfile(input_file_path):
            raise Exception('Could not find ' + input_file_path)

        self.input_file_path = input_file_path
        self.sentences_path = 'input/' + dataset_name + '/sentences_for_w2v.json'
        self.dataset_name = dataset_name
        
    def generate_vectors(self, vectors_file_path):
        if not os.path.isfile(self.sentences_path):
            self.__generate_sentences_file()
        
        WordToVec.write_vectors(self.sentences_path, vectors_file_path)

    def __generate_sentences_file(self):
        logger.info('Reading corpus file and preprocessing')
        lines = utils.read_file(self.input_file_path).split("\n")
        if self.dataset_name == 'quran':
            lines_tokenized = [[word.lower() for word in nltk.word_tokenize(line) if word] for line in lines if line]
        else:
            lines_tokenized = [[word.lower() for word in nltk.word_tokenize(line) if word.isalpha()] for line in lines
                               if line]

        utils.save_json(self.sentences_path, lines_tokenized)
        logger.info('Finished. Saving sentences for later use in word2vec')
        return True

    @staticmethod
    def write_vectors(sentences_file_path, vectors_file_path):

        sentences = utils.load_json(sentences_file_path)
        
        print(len(sentences))

        model = Word2Vec(sentences, vector_size=100, window=15, min_count=1, workers=4)
        #model.save("word2vec.model")
        #model = Word2Vec.load("word2vec.model")

        lines = []
        for key in model.wv.index_to_key:
            lines.append(key + ' ' + ' '.join(['{:.6f}'.format(f) for f in model.wv[key].tolist()]))

        fp = open(vectors_file_path, '+w')
        fp.write("\r\n".join(lines))
        fp.close()


if __name__ == '__main__':

    WordToVec.write_vectors('input/cnn/sentences_for_w2v.json', 'input/cnn/vectors/w2v.txt')