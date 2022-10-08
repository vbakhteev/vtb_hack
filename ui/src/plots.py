import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_trends(topics_data):
    df_trend = pd.DataFrame([
        {'trend_value': topic_data['trend_value'], 'name': topic_data['name']} for topic_data in topics_data
    ])
    df_trend = df_trend.sort_values('trend_value', ascending=False)
    df_trend['positive'] = df_trend['trend_value'] > 0

    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    sns.barplot(
        data=df_trend,
        x='trend_value',
        y='name',
        palette=df_trend.positive.map({True: 'g', False: 'r'}),
        ax=ax,
    )
    ax.set_ylabel('')
    ax.get_xaxis().set_visible(False)
    ax.set_xlabel('Тренд')
    return fig


def get_occurences_data(topics_data):
    months = sorted({
        freq['month'] for topic in topics_data for freq in topic['frequency']
    })

    columns = {'months': months}
    for topic in topics_data:
        name = topic['name']
        frequency = topic['frequency']

        counts = []
        for month in months:
            topic_month = [mc for mc in frequency if mc['month'] == month] or None
            if topic_month is None:
                count = 0
            else:
                count = topic_month[0]['count']
            
            counts.append(count)

        columns[name] = counts

    chart_data = pd.DataFrame(columns)

    return chart_data
