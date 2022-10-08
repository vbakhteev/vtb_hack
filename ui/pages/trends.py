from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src import client
from src.consts import ROLE_MAPPING
from src.plots import plot_trends, get_occurences_data
from src.preprocessing import get_trend_data


st.title('Параметры')
role = st.radio("Роль", ROLE_MAPPING.keys())
role_name = ROLE_MAPPING[role]

slider = st.slider(
    'Считать тренд с какого месяца?',
    min_value=datetime(year=2020, month=10, day=1).date(),
    max_value=datetime.now().date(),
    step=timedelta(days=30),
    format="MM/YY",
)

all_topics = client.get_topics(role_name=role_name)
topic_names = st.multiselect(
    'Выбрать темы для анализа',
    [topic['name'] for topic in all_topics],
    [topic['name'] for topic in all_topics],
)

topics_data = get_trend_data(topic_names, all_topics, client)

st.title('Аналитика')

fig = plot_trends(topics_data)
st.pyplot(fig)

chart_data = get_occurences_data(topics_data)
st.line_chart(data=chart_data, x='months')
