import handle_file as hf
import pandas as pd
from time import sleep
from tqdm import tqdm

def identify_tweets(df, keyphrases, thresh):
    misinfo_array = []
    not_misinfo_array = []
    columns = ['tweet', 'clean', 'date', 'time', 'link']

    with tqdm(total=df.shape[0]) as pbar:
        for i, row1 in df.iterrows():
            sleep(0.1)
            line = row1['clean']
            misinfo = False
            for j, row2 in keyphrases.iterrows():
                ngram = row2['ngram']
                klipscore = row2['score']
                if ngram in line and klipscore >= thresh:
                    misinfo = True
                    misinfo_array.append([row1['tweet'], line, row1['date'], row1['time'], row1['link']])
                    break

            if not misinfo:
                not_misinfo_array.append([row1['tweet'], line, row1['date'], row1['time'], row1['link']])

            pbar.update(1)

    hf.save_to_csv(pd.DataFrame(not_misinfo_array, columns=columns),
                   'data-res/classifier-results/not-tagged-misinfo.csv')
    return pd.DataFrame(misinfo_array, columns=columns)