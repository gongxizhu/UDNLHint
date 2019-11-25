import os
import sys
sys.path.append("..")
from itertools import zip_longest
from utils.tokenizer import tokenize
# import nltk
# from nltk.tokenize import TweetTokenizer
# from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatizer


def Prepare():
    dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dirname, 'data')
    data_from_filename = 'data.from'
    data_to_filename = 'data.to'
    train_from_filename = 'train.from'
    train_to_filename = 'train.to'
    test_from_filename = 'test.from'
    test_to_filename = 'test.to'
    dev_from_filename = 'dev.from'
    dev_to_filename = 'dev.to'
    vocab_from_filename = 'vocab.from'
    vocab_to_filename = 'vocab.to'
    vocab_from = []
    vocab_to = []
    tokenized_lines_from = []
    tokenized_lines_to = []
    with open('{}/{}'.format(data_dir, data_from_filename), 'r',
        encoding='utf-8', buffering=131072) as data_from_in:
        lines = ReadLines(data_from_in)
        for line in lines:
            tokenized_lines_from.append(tokenize(line))

    with open('{}/{}'.format(data_dir, data_to_filename), 'r',
        encoding='utf-8', buffering=131072) as data_to_in:
        lines = ReadLines(data_to_in)
        for line in lines:
            words = line.split()
            sentence = " ".join(words)
            sentence = sentence.strip()
            tokenized_lines_to.append(sentence)

    # Create vocab from
    vocab_from = GetVocab(tokenized_lines_from)
    # Create vocab to
    vocab_to = GetVocab(tokenized_lines_to)

    count_data = len(tokenized_lines_from)
    count_train = int(count_data * 0.7) # 70% to train
    count_dev = int(count_data * 0.2) # 20% to dev
    count_test = count_data - count_train - count_dev # 10% to test
    # Create train data from and to
    train_from = tokenized_lines_from[:count_train]
    train_to = tokenized_lines_to[:count_train]
    # Create test data from and to
    dev_from = tokenized_lines_from[count_train:count_train + count_dev]
    dev_to = tokenized_lines_to[count_train:count_train + count_dev]
    # Create dev data from and to
    test_from = tokenized_lines_from[count_train + count_dev:]
    test_to = tokenized_lines_to[count_train + count_dev:]

    with open('{}/{}'.format(data_dir, train_from_filename), 'w',
        encoding='utf-8', buffering=131072) as train_from_out:
        WriteLines(train_from_out, train_from)

    with open('{}/{}'.format(data_dir, train_to_filename), 'w',
        encoding='utf-8', buffering=131072) as train_to_out:
        WriteLines(train_to_out, train_to)

    with open('{}/{}'.format(data_dir, dev_from_filename), 'w',
        encoding='utf-8', buffering=131072) as dev_from_out:
        WriteLines(dev_from_out, dev_from)

    with open('{}/{}'.format(data_dir, dev_to_filename), 'w',
        encoding='utf-8', buffering=131072) as dev_to_out:
        WriteLines(dev_to_out, dev_to)

    with open('{}/{}'.format(data_dir, test_from_filename), 'w',
        encoding='utf-8', buffering=131072) as test_from_out:
        WriteLines(test_from_out, test_from)

    with open('{}/{}'.format(data_dir, test_to_filename), 'w',
        encoding='utf-8', buffering=131072) as test_to_out:
        WriteLines(test_to_out, test_to)

    with open('{}/{}'.format(data_dir, vocab_from_filename), 'w',
        encoding='utf-8', buffering=131072) as vocab_from_out:
        WriteLines(vocab_from_out, vocab_from)

    with open('{}/{}'.format(data_dir, vocab_to_filename), 'w',
        encoding='utf-8', buffering=131072) as vocab_to_out:
        WriteLines(vocab_to_out, vocab_to)

def ReadLines(file_in):
    lines = file_in.readlines()
    return lines

def WriteLines(file_out, lines):
    file_out.write('\n'.join(lines))

def GetVocab(lines):
    local_vocab = []
    for line in lines:
        words = [word.strip() for word in line.split(' ')]
        for word in words:
            if word not in local_vocab:
                local_vocab.append(word)

    return local_vocab

def CreateVocabTo(parts, DATs, STDs):
    local_vocab = []
    for part in parts:
        local_parts = part.split(',')
        for local_part in local_parts:
            if(len(local_part.replace('nan', '').strip()) > 0):
                if(local_part.replace('nan', '').strip() not in local_vocab):
                    local_vocab.append(local_part.replace('nan', '').strip())

    for dat in DATs:
        local_dats = dat.split(',')
        for local_dat in local_dats:
            if(len(local_dat.replace('nan', '').strip()) > 0):
                if(local_dat.replace('nan', '').strip() not in local_vocab):
                    local_vocab.append(local_dat.replace('nan', '').strip())

    for std in STDs:
        local_stds = std.split(',')
        for local_std in local_stds:
            if(len(local_std.replace('nan', '').strip()) > 0):
                if(local_std.replace('nan', '').strip() not in local_vocab):
                    local_vocab.append(local_std.replace('nan', '').strip())

    local_vocab.append('Straight')
    local_vocab.append('TextAmount')

    return local_vocab

def FilterByNLTK():
    dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dirname, 'data')
    data_from_filename = 'data.from'
    data_to_filename = 'data.to'
    train_from_filename = 'train.from'
    train_to_filename = 'train.to'
    test_from_filename = 'test.from'
    test_to_filename = 'test.to'
    dev_from_filename = 'dev.from'
    dev_to_filename = 'dev.to'
    vocab_from_filename = 'vocab.from'
    vocab_to_filename = 'vocab.to'
    vocab_from = []
    vocab_to = []
    tokenized_lines_from = []
    tokenized_lines_to = []
    with open('{}/{}'.format(data_dir, data_from_filename), 'r',
        encoding='utf-8', buffering=131072) as data_from_in:
        lines = ReadLines(data_from_in)
        for line in lines:
            tokenized_lines_from.append(tokenize(line))

    with open('{}/{}'.format(data_dir, data_to_filename), 'r',
        encoding='utf-8', buffering=131072) as data_to_in:
        lines = ReadLines(data_to_in)
        for line in lines:
            tokenized_lines_to.append(tokenize(line))

    # Create vocab from
    vocab_from = GetVocab(tokenized_lines_from)
    # Create vocab to
    vocab_to = GetVocab(tokenized_lines_to)

    count_data = len(tokenized_lines_from)
    count_train = int(count_data * 0.7) # 70% to train
    count_dev = int(count_data * 0.2) # 20% to dev
    count_test = count_data - count_train - count_dev # 10% to test
    # Create train data from and to
    train_from = tokenized_lines_from[:count_train]
    train_to = tokenized_lines_to[:count_train]
    # Create test data from and to
    dev_from = tokenized_lines_from[count_train:count_train + count_dev]
    dev_to = tokenized_lines_to[count_train:count_train + count_dev]
    # Create dev data from and to
    test_from = tokenized_lines_from[count_train + count_dev:]
    test_to = tokenized_lines_to[count_train + count_dev:]

    with open('{}/{}'.format(data_dir, train_from_filename), 'w',
        encoding='utf-8', buffering=131072) as train_from_out:
        WriteLines(train_from_out, train_from)

    with open('{}/{}'.format(data_dir, train_to_filename), 'w',
        encoding='utf-8', buffering=131072) as train_to_out:
        WriteLines(train_to_out, train_to)

    with open('{}/{}'.format(data_dir, dev_from_filename), 'w',
        encoding='utf-8', buffering=131072) as dev_from_out:
        WriteLines(dev_from_out, dev_from)

    with open('{}/{}'.format(data_dir, dev_to_filename), 'w',
        encoding='utf-8', buffering=131072) as dev_to_out:
        WriteLines(dev_to_out, dev_to)

    with open('{}/{}'.format(data_dir, test_from_filename), 'w',
        encoding='utf-8', buffering=131072) as test_from_out:
        WriteLines(test_from_out, test_from)

    with open('{}/{}'.format(data_dir, test_to_filename), 'w',
        encoding='utf-8', buffering=131072) as test_to_out:
        WriteLines(test_to_out, test_to)

    with open('{}/{}'.format(data_dir, vocab_from_filename), 'w',
        encoding='utf-8', buffering=131072) as vocab_from_out:
        WriteLines(vocab_from_out, vocab_from)

    with open('{}/{}'.format(data_dir, vocab_to_filename), 'w',
        encoding='utf-8', buffering=131072) as vocab_to_out:
        WriteLines(vocab_to_out, vocab_to)


# if __name__ == "__main__":
#     # prepare()
#     # Prepare()
#     p = "Parts 3-month inspection 3-month periodic inspection set vehicle collection fee Vehicle delivery charge"
#     words = nltk.tokenize.word_tokenize(p)
#     print(words)