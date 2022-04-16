import codecs, json
import numpy as np

'''Serializable/Pickleable class to replicate the functionality of collections.defaultdict'''
class autovivify_list(dict):
        def __missing__(self, key):
                value = self[key] = []
                return value

        def __add__(self, x):
                '''Override addition for numeric types when self is empty'''
                if not self and isinstance(x, Number):
                        return x
                raise ValueError

        def __sub__(self, x):
                '''Also provide subtraction method'''
                if not self and isinstance(x, Number):
                        return -1 * x
                raise ValueError


def build_word_vector_matrix(vector_file, n_words):
	'''Read a GloVe array from sys.argv[1] and return its vectors and labels as arrays'''
	np_arrays = []
	labels_array = []

	with codecs.open(vector_file, 'r', 'utf-8') as f:
		for i, line in enumerate(f):
			sr = line.split()
			labels_array.append(sr[0])
			np_arrays.append(np.array([float(j) for j in sr[1:]]))
			if i == n_words - 1:
				return np.array(np_arrays), labels_array
		return np.array(np_arrays), labels_array


def get_cache_filename_from_args(args):
        a = (args.vector_dim, args.num_words, args.num_clusters)
        return '{}D_{}-words_{}-clusters.json'.format(*a)


def get_label_dictionaries(labels_array):
        id_to_word = dict(zip(range(len(labels_array)), labels_array))
        word_to_id = dict((v,k) for k,v in id_to_word.items())
        return word_to_id, id_to_word


def save_json(filename, results):
        with open(filename, 'w') as f:
                json.dump(results, f, ensure_ascii=False)


def load_json(filename):
        with open(filename, 'r') as f:
                return json.load(f)


def read_file(path):
    file = open(path, "r")
    content = file.read()
    return content


def write_file(path, content):
    file = open(path, "w")
    content = file.write(content)
    file.close()
    return content


def print_vocab_stats():
    import os
    datasets = [item for item in os.listdir('input') if os.path.isdir('input/' + item)]
    for dataset_name in datasets:
        file_path = f'input/{dataset_name}/vocab.txt'
        content = read_file(file_path)
        lines = content.split("\n")
        line_words = [line.split() for line in lines]
        counts = [int(words[1]) for words in line_words if len(words)>0]
        lengths = [len(words[0]) for words in line_words if len(words)>0]
        total_words = sum(counts)
        print(f"#words in dataset {dataset_name}: ", total_words)
        print(f"Mean word length in dataset {dataset_name}: ", sum(lengths)/len(lengths))


if __name__ == '__main__':
    print_vocab_stats()

