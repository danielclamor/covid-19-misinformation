try:
    tl_stopwords = open('data-res/stopwords_tl-modified.txt', encoding='utf-8-sig').read().splitlines()
except FileNotFoundError:
    print('File not found!')

try:
    gram_coh = open('data-res/gram-coh.txt', encoding='utf-8-sig').read().splitlines()
except FileNotFoundError:
    print('File not found!')

try:
    differentials = open('data-res/differential.txt', encoding='utf-8-sig').read().splitlines()
except FileNotFoundError:
    print('File not found!')

try:
    typicals = open('data-res/typical.txt', encoding='utf-8-sig').read().splitlines()
except FileNotFoundError:
    print('File not found!')

try:
    keywords = open('data-res/keywords.txt', encoding='utf-8-sig').read().splitlines()
except FileNotFoundError:
    print('File not found!')
