import streamlit as st
import pandas as pd

from src import client
from src import templates
from src.preprocessing import feed
from src.consts import SHOW_NUM_NEWS, ROLE_MAPPING


role = st.radio("Роль", ROLE_MAPPING.keys())
role_name = ROLE_MAPPING[role]

topics = client.get_topics(role_name)

topic_name = st.selectbox('Выбрать тему', [topic['name'] for topic in topics])

topic_id = [t for t in topics if t['name'] == topic_name][0]['topic_id']

frequency = client.get_trend(topic_id=topic_id)
ts_data = pd.DataFrame(frequency)

st.header('Встречаемость темы')
st.area_chart(data=ts_data, x='month', y='count')

publications = client.get_publications(topic_id=topic_id, num=SHOW_NUM_NEWS)
for html in feed(publications):
    st.write(html, unsafe_allow_html=True)
