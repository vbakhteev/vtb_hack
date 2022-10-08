import streamlit as st
import pandas as pd

from src import client
from src import templates
from src.preprocessing import feed
from src.consts import SHOW_NUM_NEWS, ROLE_MAPPING


role = st.radio("Роль", ROLE_MAPPING.keys())
role_name = ROLE_MAPPING[role]

topics = client.get_topics(role_name)
tabs = st.tabs([topic['name'] for topic in topics])

for tab, topic in zip(tabs, topics):
    topic_id = topic['topic_id']

    with tab:
        frequency = client.get_trend(topic_id=topic_id)
        ts_data = pd.DataFrame(frequency)

        st.header('Встречаемость темы')
        st.area_chart(data=ts_data, x='month', y='count')


        publications = client.get_publications(topic_id=topic_id, num=SHOW_NUM_NEWS)

        for html in feed(publications):
            st.write(html, unsafe_allow_html=True)
