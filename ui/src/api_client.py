import requests
from typing import Literal
from urllib.parse import urljoin


class ApiClient:
    def __init__(self, url):
        self.url = url

    def get_topics(self, role_name: Literal["manager", "accountant"]):
        topics = self._get(
            'topics',
            {'role_name': role_name},
        )

        return topics
    
    def get_publications(self, topic_id: int, num: int):
        publications = self._get(
            'publications',
            {'topic_id': topic_id, 'num': num},
        )
        return publications

    def get_trend(self, topic_id: int):
        trend = self._get(
            'trend',
            {'topic_id': topic_id}
        )
        return trend["frequency"]

    def _get(self, endpoint, params):
        response = requests.get(
            urljoin(self.url, endpoint),
            params=params
        )
        response.raise_for_status()

        return response.json()
