import streamlit as st
import handle_file as hf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('UTF-8-SIG')

def data_view():
    st.set_page_config(page_title='Twitter Data',
                       layout='wide',
                       page_icon='🐦')
    st.title('🐦 Twitter Data')

    twitter_data = hf.read_from_csv('data-res/files-needed/twitter-data-with-datetime.csv')
    unlabeled_data = hf.read_from_csv('data-res/files-needed/unlabeled-data.csv')
    misinfo_data = hf.read_from_csv('data-res/files-needed/misinfo-training-data.csv')
    not_misinfo_data = hf.read_from_csv('data-res/files-needed/not-misinfo-training-data.csv')
    misinfo_klip = hf.read_from_csv('data-res/files-needed/misinfo-klip-with-datetime.csv')

    cola, colb = st.columns(2)
    with cola:
        st.caption('Data collected from January 1, 2020 to March 22, 2020')
        st.dataframe(twitter_data)
        st.download_button(label='Download',
                           data=convert_df(twitter_data),
                           file_name='twitter-data.csv',
                           mime='text/csv')
    with colb:
        line_twitter_data = twitter_data.value_counts(subset='date',
                                                      sort=False).\
            rename_axis('date').reset_index(name='count')
        twitter_line_graph = px.line(line_twitter_data,
                                     x='date',
                                     y='count',
                                     title='COVID-19 Tweet Count per Day')
        st.plotly_chart(twitter_line_graph)

    st.subheader('Labeled and Unlabeled Data')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('Misinformation Data')
        st.dataframe(misinfo_data)
        st.download_button(label='Download',
                           data=convert_df(misinfo_data),
                           file_name='misinfo-data.csv',
                           mime='text/csv')

    with col2:
        st.markdown('Not Misinformation Data')
        st.dataframe(not_misinfo_data)
        st.download_button(label='Download',
                           data=convert_df(not_misinfo_data),
                           file_name='not-misinfo-data.csv',
                           mime='text/csv')

    with col3:
        st.markdown('Unlabeled Data')
        st.dataframe(unlabeled_data)
        st.download_button(label='Download',
                           data=convert_df(unlabeled_data),
                           file_name='unlabeled-data.csv',
                           mime='text/csv')

    st.subheader('Identifier Result')
    col4, col5 = st.columns(2)
    with col4:
        st.markdown('Misinformation tweets found from Unlabeled Data')
        st.dataframe(misinfo_klip)
        st.download_button(label='Download',
                           data=convert_df(misinfo_klip),
                           file_name='misinfo-klip-with-datetime.csv',
                           mime='text/csv')

    with col5:
        line_data = misinfo_klip.value_counts(subset='date', sort=False).\
            rename_axis('date').reset_index(name='count')
        line_graph = px.line(line_data,
                             x='date',
                             y='count',
                             title='COVID-19 Misinformation Tweet Count per Day')

        st.plotly_chart(line_graph)


data_view()