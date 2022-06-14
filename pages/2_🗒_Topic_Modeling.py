import streamlit as st
import handle_file as hf
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from time import sleep

def get_bow(tweets):
    a_list = []
    prog_bar = st.progress(0)
    for i, tweet in enumerate(tweets):
        sleep(0.1)
        for word in tweet.split(' '):
            a_list.append(word)
        prog_bar.progress(i)
    prog_bar.empty()
    return ', '.join(a_list)

def btm_view():
    st.set_page_config(page_title='Topic Modeling',
                       layout='wide',
                       page_icon='🗒️')
    st.title('🗒️ Topic Modeling')

    topic_models_labels = hf.read_from_csv('data-res/files-needed/topicmodels-labels.csv')
    tweets_topics = hf.read_from_csv('data-res/files-needed/tweets-topics.csv')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Labeled topic models')
        st.dataframe(topic_models_labels.set_index('topic'))

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('Tweets and corresponding topic')
        st.dataframe(tweets_topics)

    with col4:
        topics = topic_models_labels['topic'].tolist()
        labels = topic_models_labels['label'].tolist()
        topic_count = tweets_topics['topic'].value_counts(sort=False).tolist()

        pie_data = pd.DataFrame({'Topic': topics,
                                 'Label': labels,
                                 'Tweet Count': topic_count})
        pie_graph = px.pie(pie_data,
                           values='Tweet Count',
                           names='Label',
                           hole=.3,
                           title='Common Topics for COVID-19 Misinformation Tweets 2020',
                           hover_data=['Topic'])

        st.plotly_chart(pie_graph, use_container_width=True)

    col5, col6 = st.columns(2)
    narrative_df = hf.read_from_csv('data-res/files-needed/narratives.csv')
    with col5:
        narrative = st.selectbox('Choose a narrative',
                                 narrative_df['narrative'])
    with col6:
        desc = narrative_df['description'].\
            loc[narrative_df['narrative'] == narrative].values[0]
        st.text_area(narrative, value=desc)

    with col2:
        sb_display = ['Topic {}'.format(i) for i in topic_models_labels['topic']]
        topic = st.selectbox('Topic Wordcloud',
                             topic_models_labels['topic'],
                             format_func=lambda x: sb_display[x-1])
        text = get_bow(tweets_topics.query('topic == {}'.format(topic))['clean'])
        wc = WordCloud(max_words=50).generate(text)
        wc_graph, ax = plt.subplots(figsize=(20, 10),
                                    facecolor='k')
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        st.pyplot(wc_graph)


btm_view()