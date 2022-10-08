from typing import List

import numpy as np
from sklearn.linear_model import LinearRegression

from src.api_client import ApiClient
from src import templates


def get_trend_data(topic_names: List[str], all_topics: List[dict], first_month: str, client: ApiClient):
    topics_data = []
    for topic_name in topic_names:
        topic = [topic for topic in all_topics if topic_name == topic['name']][0]
        topic_id = topic['topic_id']

        frequency = client.get_trend(topic_id)
        frequency = [x for x in frequency if x['month'] > first_month]
        if len(frequency) < 2:
            continue

        trend_value = compute_trend_value(
            [x['count'] for x in frequency]
        )

        topics_data.append({
            'name': topic_name,
            'frequency': frequency,
            'trend_value': trend_value,
        })

    return topics_data


def compute_trend_value(counts: List[int]) -> float:
    x = np.arange(len(counts)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, counts)
    trend_value = model.coef_[0]

    return trend_value


def feed(publications):
    for i, publication in enumerate(publications):
        url = publication['url']
        title = publication['title']
        text = publication['text'].replace('\n', ' ').split()
        highlights = ' '.join(text[:40]) + '...'
        num_minutes = max(round(len(text) / 120), 1)
        html = templates.search_result(i, url=url, title=title, highlights=highlights, author='', length=f'{num_minutes} минут')

        yield html
