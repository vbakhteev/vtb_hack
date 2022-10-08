from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Параметры')

role = st.radio("Роль", ["Гендир", "Бухгалтер"])

slider = st.slider(
    'Считать тренд с какого месяца?',
    min_value=datetime(year=2020, month=10, day=1).date(),
    max_value=datetime.now().date(),
    step=timedelta(days=30),
    format="MM/YY",
)

all_topic_names = ['Спорт', 'Политика', 'Погода']
topic_names = st.multiselect(
    'Выбрать темы для анализа',
    all_topic_names,
    all_topic_names,
)

st.title('Аналитика')

rows = []
i = 0
for topic_name in topic_names:
    rows.append({
        'topic_name': topic_name,
        'trend_value': i,
    })
    i += 1
df_trend = pd.DataFrame(rows)
df_trend = df_trend.sort_values('trend_value', ascending=False)
df_trend['positive'] = df_trend['trend_value'] > 0

fig = plt.figure(figsize=(12,8))
fig, ax = plt.subplots(1, 1)
sns.barplot(
    data=df_trend,
    x='trend_value',
    y='topic_name',
    palette=df_trend.positive.map({True: 'g', False: 'r'}),
    ax=ax,
)
ax.set_ylabel('')
ax.get_xaxis().set_visible(False)
ax.set_xlabel('Тренд')
st.pyplot(fig)

chart_data = pd.DataFrame({
    'month': ['2022-06', '2022-07', '2022-08', '2022-09'],
    'Спорт': [10, 20, 30, 40],
    'Политика': [40, 30, 20, 10],
    'Погода': [10, 10, 10, 100],
})
chart_data = chart_data[['month'] + topic_names]
st.line_chart(data=chart_data, x='month')
