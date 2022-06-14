import numpy as np
import pyLDAvis
import pandas as pd
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms, topic_summuary

def do_btm(df, num_topics, num_iter, topic_coh=10, ldavis_path='ldavis-btm.html'):
    clean = df['clean'].tolist()
    print(clean)
    original = df['tweet'].tolist()
    print(original)

    # vectorize texts
    vec = CountVectorizer()
    X = vec.fit_transform(clean).toarray()

    # get biterms
    biterms = vec_to_biterms(X)

    # check if there is null
    keys = []
    for i, line in enumerate(biterms):
        if line:
            continue
        else:
            keys.append(i)

    if keys:
        print(keys)

        # delete invalid lines
        clean = np.delete(clean, [keys])
        original = np.delete(original, [keys])

        # vectorize texts
        vec = CountVectorizer()
        X = vec.fit_transform(clean).toarray()

        # get biterms
        biterms = vec_to_biterms(X)

    print('len of clean texts:', len(clean))
    print('len of original texts:', len(original))
    print('len of X:', X.shape)
    print('len of biterms:', len(biterms))

    # get vocabulary
    vocab = np.array(vec.get_feature_names())
    print('len of vocab:', vocab.shape)

    # create model
    btm = oBTM(num_topics=num_topics, V=vocab)

    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100): # process chunk of 200 texts
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=num_iter)
    topics = btm.transform(biterms)
    print(topics)
    print(topics.shape)

    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0))
    pyLDAvis.save_html(vis, ldavis_path)  # path to output

    print("\n\n Texts & Topics ..")
    an_array = []
    columns = ['tweet', 'clean', 'topic']
    for i in range(len(clean)):
        print("{} (topic: {})".format(clean[i], topics[i].argmax()))
        an_array.append([original[i], clean[i], topics[i].argmax()+1])

    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X, vocab, topic_coh)

    return pd.DataFrame(an_array, columns=columns)