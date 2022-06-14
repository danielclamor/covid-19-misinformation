import re
from nltk.tokenize import RegexpTokenizer, TreebankWordTokenizer
from nltk.corpus import stopwords
from import_txt import tl_stopwords, gram_coh, differentials, typicals, keywords
from collections import Counter
from time import sleep
from stqdm import stqdm
import pandas as pd

def tokenize_line(line):
    tokenizer = TreebankWordTokenizer()
    tokens = tokenizer.tokenize(line)
    line = ' '.join(tokens)

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(line)

    return tokens

def normalize_line(line):
    line = re.sub(r'http\S+', '', line)  # remove urls
    line = re.sub('[@]\w+', '', line)  # remove mentions
    line = re.sub('[#]\w+', '', line)  # remove hashtags
    line = re.sub(r'[^\x00-\x7F]+', '', line)  # remove non-ascii
    line = re.sub('_', '', line)  # remove underscore
    return line.lower()

def is_stopword(token):
    if token in stopwords.words() or token in tl_stopwords:
        return True
    else:
        return False

def is_keyword(token):
    if token in keywords:
        return True
    else:
        return False

def is_typical(token):
    if token in typicals:
        return True
    else:
        return False

def is_differential(token):
    if token in differentials:
        return True
    else:
        return False

def is_gramcoh(token):
    if token in gram_coh:
        return True
    else:
        return False

def get_common_words(a_list, no_of_words):
    bow = ' '.join(a_list)
    print(bow.split())
    word_counter = Counter(bow.split())
    '''common = []
    for tup in word_counter.most_common(no_of_words):
        common.append(tup[0])'''
    common_words = []
    for word in word_counter.most_common(no_of_words):
        print(word)
        common_words.append(word[0])

    return common_words

def preprocess_text(line, min_char_len=2, forBTM=False, common_words=None):
    # remove_words = 3 for stopwords, gramcoh, and keywords
    # 2 for stopwords and gramcoh
    # 1 for stopwords
    clean_tokens = []
    tokens = tokenize_line(normalize_line(line))

    if tokens:
        for token in tokens:
            token = re.sub(r'\b[0-9]+\b\s*', '', token)  # remove digit only words
            if len(token) >= min_char_len:
                if forBTM:
                    if common_words:
                        if token not in common_words:
                            clean_tokens.append(token)
                    else:
                        clean_tokens.append(token)
                else:
                    if not is_stopword(token):
                        clean_tokens.append(token)

        if len(clean_tokens) >= 2:
            return ' '.join(clean_tokens)
        else:
            return None

def prepare_df(df):
    an_array = []
    columns = ['tweet', 'clean', 'link']

    with stqdm(total=df.shape[0]) as pbar:
        for i, row in df.iterrows():
            sleep(0.1)
            line = row['tweet']
            clean_row = preprocess_text(line)
            if clean_row:
                an_array.append([clean_row, line, row['link']])

            pbar.update(1)

    return pd.DataFrame(an_array, columns=columns)

def prepare_for_btm(df):
    common_words = get_common_words(df['clean'], 15)
    an_array = []
    columns = ['tweet', 'clean']

    with stqdm(total=df.shape[0]) as pbar:
        for i, row in df.iterrows():
            sleep(0.1)
            line = row['clean']
            clean_row = preprocess_text(line,
                                        min_char_len=4,
                                        forBTM=True,
                                        common_words=common_words)
            if clean_row:
                an_array.append([clean_row, line])

            pbar.update(1)

    return pd.DataFrame(an_array, columns=columns)