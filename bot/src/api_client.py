import requests
from urllib.parse import urljoin


class ApiClient:
    def __init__(self, host):
        self.host = host
        self.register_endpoint = '/register'
        self.recommend_endpoint = '/recommend'
        self.save_event_endpoint = '/save_event'
        self.publication_url_endpoint = '/publication_url'

    def register(self, user_id: int, full_name: str, user_type: str):
        self._post(
            self.register_endpoint,
            {"user_id": user_id, "full_name": full_name, "user_type": user_type},
        )

    def save_event(self, user_id: int, publication_id: int, event_type: str):
        self._post(
            self.save_event_endpoint,
            {"user_id": user_id, "publication_id": publication_id, "event_type": event_type},
        )

    def recommend(self, user_id: int) -> dict:
        data = self._get(
            self.recommend_endpoint,
            params={'user_id': user_id},
        )
        return data

    def get_publication_url(self, publication_id: int) -> str:
        data = self._get(
            self.publication_url_endpoint,
            params={'publication_id': publication_id},
        )
        return data

    def _post(self, endpoint, data):
        url = urljoin(self.host, endpoint)

        response = requests.post(
            url=url,
            json=data,
        )
        response.raise_for_status()
        return response.json()
    
    def _get(self, endpoint, params):
        url = urljoin(self.host, endpoint)

        response = requests.get(
            url=url,
            params=params,
        )

        response.raise_for_status()
        return response.json()
