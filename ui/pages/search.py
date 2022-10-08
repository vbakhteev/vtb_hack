import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src import client
from src import templates
from src.consts import SHOW_NUM_NEWS


st.title('Поиск новостей по своей теме')
query = st.text_input('Введите запрос')

if len(query):
    st.write(templates.load_css(), unsafe_allow_html=True)
    start_time = time.time()
    publications, tags = client.search(query, num=SHOW_NUM_NEWS)
    took = time.time() - start_time

    total_hits = len(publications)
    # show number of results and time taken
    st.write(templates.number_of_results(total_hits, took),
                unsafe_allow_html=True)

    # render popular tags as filters
    st.write(templates.tag_boxes(query, tags, ''),
                unsafe_allow_html=True)

    # search results
    for i, publication in enumerate(publications):
        url = publication['url']
        title = publication['title']
        text = publication['text'].replace('\n', ' ').split()
        highlights = ' '.join(text[:40]) + '...'
        num_minutes = max(round(len(text) / 120), 1)

        st.write(templates.search_result(i, url=url, title=title, highlights=highlights, author='', length=f'{num_minutes} минут'), unsafe_allow_html=True)