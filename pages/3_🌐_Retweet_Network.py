import pandas as pd
import streamlit as st
import handle_file as hf
import plotly.express as px
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
from stqdm import stqdm
from time import sleep

def create_routing_table(nodes, edges):
    adj_matrix = []

    size = len(nodes)
    for i in range(size):
        adj_matrix.append([0 for j in range(size)])

    with stqdm(total=len(edges)) as pbar:
        for edge in edges:
            sleep(0.1)
            from_node = edge[0]
            to_node = edge[1]
            adj_matrix[nodes.index(from_node)][nodes.index(to_node)] += 1
            pbar.update(1)

    return pd.DataFrame(adj_matrix, index=nodes, columns=nodes)

def sna_view():
    
    st.set_page_config(page_title='Retweet Network',
                       layout='wide',
                       page_icon='🌐')
    st.title('🌐 Retweet Network')

    uploaded_file = st.file_uploader('Upload twitter data',
                                     type='csv',
                                     key='uploaded_file')
    tweet_details_df = pd.DataFrame()

    if uploaded_file:
        tweet_details_df = hf.read_from_csv(uploaded_file)

    if tweet_details_df.empty is False:
        G = nx.DiGraph()
        adj_nodes = []
        adj_edges = []
        with stqdm(total=tweet_details_df.shape[0]) as pbar:
            for i, row in tweet_details_df.iterrows():
                sleep(0.1)
                from_node = str(row['author_id'].strip('[]'))
                if from_node not in adj_nodes:
                    adj_nodes.append(from_node)
                retweeters = (row['retweeters'].strip('[]')).split(' ')
                for rt_id in retweeters:
                    if rt_id:
                        to_node = str(rt_id)
                        if G.has_edge(from_node, to_node):
                            G.edges[from_node, to_node]['weight'] += 1
                        G.add_edge(from_node, to_node, weight=1)
                        if to_node not in adj_nodes:
                            adj_nodes.append(to_node)
                        adj_edges.append((from_node, to_node))
                pbar.update(1)

        nodes = [Node(id=i, label=str(i), size=200) for i in G.nodes]
        edges = [Edge(source=i, target=j) for (i, j) in G.edges
                 if i in G.nodes and j in G.nodes]

        config = Config(width=1500,
                        height=500,
                        directed=True,
                        nodeHighlightBehavior=False,
                        highlightColor="#F7A7A6",  # or "blue"
                        collapsible=False,
                        node={'labelProperty': 'label'},
                        # **kwargs e.g. node_size=1000 or node_color="blue"
                        )

        return_value = agraph(nodes=nodes,
                              edges=edges,
                              config=config)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Nodes: {} || Edges: {}'.format(len(nodes), len(edges)))

        with col2:
            with st.expander('Out-degree'):
                out_degree_df = pd.DataFrame(G.out_degree,
                                             columns=['node', 'out_degree']).sort_values(by=['out_degree'],
                                                                                         ascending=False)
                st.dataframe(out_degree_df)

        with col3:
            with st.expander('In-degree'):
                in_degree_df = pd.DataFrame(G.in_degree,
                                            columns=['node', 'in_degree']).sort_values(by=['in_degree'],
                                                                                       ascending=False)
                st.dataframe(in_degree_df)

        col4, col5 = st.columns(2)
        with col4:
            with_retweet = out_degree_df['node'].loc[out_degree_df['out_degree'] > 0].count()
            without_retweet = out_degree_df['node'].loc[out_degree_df['out_degree'] == 0].count()
            pie_data = pd.DataFrame({'Source': ['With Retweets', 'Without Retweets'],
                                     'Count': [with_retweet, without_retweet]})
            pie_graph = px.pie(pie_data,
                               values='Count',
                               names='Source',
                               hole=.3,
                               title='Users who got atleast one retweet',
                               color_discrete_sequence=px.colors.sequential.Aggrnyl)

            st.plotly_chart(pie_graph, use_container_width=True)

        with col5:
            retweeted = in_degree_df['node'].loc[in_degree_df['in_degree'] > 0].count()
            not_retweeted = in_degree_df['node'].loc[in_degree_df['in_degree'] == 0].count()
            pie_data2 = pd.DataFrame({'User': ['Retweeted', 'Not Retweeted'],
                                     'Count': [retweeted, not_retweeted]})
            pie_graph2 = px.pie(pie_data2,
                                values='Count',
                                names='User',
                                hole=.3,
                                title='Users who retweeted atleast once',
                                color_discrete_sequence=px.colors.sequential.Agsunset)

            st.plotly_chart(pie_graph2, use_container_width=True)

        with st.expander('See routing table'):
            routing_df = create_routing_table(adj_nodes, adj_edges)
            if routing_df.empty is False:
                st.dataframe(routing_df)
            else:
                st.write('No routing table available')

        with st.expander('See tweet details'):
            tweet_df = tweet_details_df.filter(items=['tweet', 'link', 'author_id', 'retweeters'])
            st.dataframe(tweet_df)


sna_view()