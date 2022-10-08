import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src import search_client
from src import templates
from src.preprocessing import feed
from src.consts import SHOW_NUM_NEWS, ROLE_MAPPING


st.title('Поиск новостей по своей теме')

role = st.radio("Роль", ROLE_MAPPING.keys())
role_name = ROLE_MAPPING[role]

query = st.text_input('Введите запрос')

if len(query):
    st.write(templates.load_css(), unsafe_allow_html=True)
    start_time = time.time()
    publications, tags = search_client.search(query, num=SHOW_NUM_NEWS, role_name=role_name)
    took = time.time() - start_time

    total_hits = len(publications)
    # show number of results and time taken
    st.write(templates.number_of_results(total_hits, took),
                unsafe_allow_html=True)

    # render popular tags as filters
    st.write(templates.tag_boxes(query, tags, ''),
                unsafe_allow_html=True)

    # search results
    for html in feed(publications):
        st.write(html, unsafe_allow_html=True)
