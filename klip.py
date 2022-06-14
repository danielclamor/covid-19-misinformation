from nltk.lm import MLE, KneserNeyInterpolated, preprocessing
from numpy import log
from pandas import DataFrame

def pw_kl(p, q):
    return p*log(p/q)

def create_lm(text, n):
    text = [line.split() for line in text]
    training_data, padded_sents = preprocessing.padded_everygram_pipeline(n, text)
    model = MLE(n)
    model.fit(training_data, padded_sents)

    return model

def get_klip_score(fg, bg):
    n = 2
    an_array = []
    columns = ['ngram', 'freq_fg', 'relfreq_fg', 'freq_bg', 'relfreq_bg', 'phrase', 'inform', 'score']
    bigrams = []

    # make every line into a list
    text_fg = [line.split() for line in fg]
    text_bg = [line.split() for line in bg]

    # pre-process fg and bg by padding
    train_data_fg, padded_sents_fg = preprocessing.padded_everygram_pipeline(n, text_fg)
    train_data_bg, padded_sents_bg = preprocessing.padded_everygram_pipeline(n, text_bg)

    # instantiate models (unsmoothed and smoothed)
    mle_model = MLE(n)
    kn_model = KneserNeyInterpolated(n)

    # train fg corpus (unsmoothed)
    mle_model.fit(train_data_fg, padded_sents_fg)

    # train bg corpus (smoothed)
    kn_model.fit(train_data_bg, padded_sents_bg)

    # loop through every word pairs
    for line in text_fg:
        for x in range(len(line) - 1):
            w0 = line[x]
            w1 = line[x + 1]
            bigram = w0 + ' ' + w1
            if bigram not in bigrams:
                bigrams.append(bigram)
                freq_fg = mle_model.counts[[w0]][w1]
                freq_bg = kn_model.counts[[w0]][w1]

                # phraseness
                p = mle_model.score(w1, w0.split())
                q = mle_model.score(w0)*mle_model.score(w1)
                p_score = pw_kl(p, q)

                # informativeness
                q = kn_model.score(w1, w0.split())
                i_score = pw_kl(p, q)

                # combine p and i scores
                # KLIP score
                combi_score = p_score + i_score

                # store in array
                an_array.append([bigram, freq_fg, p*100, freq_bg, q*100, p_score, i_score, combi_score])

    return DataFrame(an_array, columns=columns).sort_values(by=['score'], ascending=False)

def get_keyphrases(df_fg, df_bg):
    fg_corpus = df_fg['clean']
    bg_corpus = df_bg['clean']

    count = 0
    for line in fg_corpus:
        count += len(line.split())

    count = 0
    for line in bg_corpus:
        count += len(line.split())

    klip_df = get_klip_score(fg_corpus, bg_corpus)
    return klip_df