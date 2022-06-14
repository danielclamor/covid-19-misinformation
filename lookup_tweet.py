import requests
import os
import json
import pandas as pd
import handle_file as hf
from tqdm import tqdm
from time import sleep

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

max_tries = 5
wait_sec = 5
bt = ''

def auth():
    return os.environ.get("BEARER_TOKEN", bt)

def create_url_for_fields(tweet_id):
    tweet_fields = "tweet.fields=lang,author_id,created_at,public_metrics"
    expansions = "expansions=geo.place_id"
    place_fields = "place.fields=full_name"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    # ids = "ids=1278747501642657792"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets/{}?{}&{}&{}".format(tweet_id, tweet_fields,
                                                                expansions, place_fields)
    return url

def create_url_for_rts(tweet_id):
    count = '100'
    url = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json?id={}&count={}&stringify_ids=true'\
        .format(tweet_id, count)
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    for i in range(max_tries):
        try:
            response = requests.request("GET", url, headers=headers)
            # print(response.status_code)
            if response.status_code != 200:
                '''raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )'''
                print(response.status_code, response.text)
                return {}
            return response.json()
        except requests.exceptions.ConnectionError:
            print('connection failed')
        sleep(wait_sec)

def create_df_from_response(bearer_token, df):
    an_array = []
    columns = ['tweet', 'from_GOT3', 'link', 'author_id', 'created_at', 'retweeters', 'public_metrics']
    headers = create_headers(bearer_token)
    with tqdm(total=df.shape[0]) as pbar:
        for index, row in df.iterrows():
            sleep(1)
            link = row['link']
            tweet = row['tweet']
            tweet_id = link.split('status/')[1]

            text = ''
            author_id = ''
            created_at = ''
            public_metrics = ''

            url = create_url_for_fields(tweet_id)
            json_response = connect_to_endpoint(url, headers)

            try:
                if json_response:
                    data = json_response['data']
                    text = data['text']
                    author_id = data['author_id']
                    created_at = data['created_at']
                    public_metrics = data['public_metrics']

            except KeyError:
                continue

            url = create_url_for_rts(tweet_id)
            json_response = connect_to_endpoint(url, headers)
            rt_id = []

            if json_response == '':
                rt_id.append('')

            elif json_response:
                for data in json_response['ids']:
                    rt_id.append(str(int(data)))
            an_array.append([text, tweet, link, '[{}]'.format(author_id), created_at,
                             '[{}]'.format(' '.join(rt_id)), public_metrics])
            pbar.update(1)

    return pd.DataFrame(an_array, columns=columns)

def main(path, to_path):
    bearer_token = auth()
    df = hf.read_from_csv(path).drop_duplicates(subset=['link'])
    new_df = create_df_from_response(bearer_token, df)
    hf.save_to_csv(new_df, to_path)