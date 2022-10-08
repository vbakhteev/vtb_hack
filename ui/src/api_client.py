import requests
from typing import Literal
from urllib.parse import urljoin


Role = Literal["manager", "accountant"]


class ApiClient:
    def __init__(self, url):
        self.url = url

    def get_topics(self, role_name: Role):
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
    
    def search(self, query, num: int, role_name: Role):
        response = self._get(
            'search',
            {'query': query, 'num': num, 'role_name': role_name},
        )
        publications = response['publications']
        tags = response['similar_names']

        return publications, tags

    def _get(self, endpoint, params):
        response = requests.get(
            urljoin(self.url, endpoint),
            params=params
        )
        response.raise_for_status()

        return response.json()
