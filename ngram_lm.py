import collections
import pickle

import nltk
from tqdm import tqdm

from config import pickle_file

with open(pickle_file, 'rb') as file:
    data = pickle.load(file)
char_list = data['IVOCAB']
vocab_size = len(char_list)
samples = data['train']
bigram_counter = collections.Counter()

for sample in tqdm(samples):
    text = sample['trn']
    # text = [char_list[idx] for idx in text]
    tokens = list(text)
    bigrm = nltk.bigrams(tokens)
    # print(*map(' '.join, bigrm), sep=', ')

    # get the frequency of each bigram in our corpus
    bigram_counter.update(bigrm)

# what are the ten most popular ngrams in this Spanish corpus?
print(bigram_counter.most_common(10))

bigram_freq = dict()
for key, value in bigram_counter.items():
    bigram_freq[key] = value

print('smoothing')
for i in tqdm(range(vocab_size)):
    for j in range(vocab_size):
        if (i, j) not in bigram_freq:
            bigram_freq[(i, j)] = 1

print('freq -> prob')
for i in tqdm(range(vocab_size)):
    total = 0
    for j in range(vocab_size):
        total += bigram_freq[(i, j)]
    for j in range(vocab_size):
        bigram_freq[(i, j)] = bigram_freq[(i, j)] / total

with open('bigram_freq.pkl', 'wb') as file:
    pickle.dump(bigram_freq, file)

print(bigram_freq.items()[:100])