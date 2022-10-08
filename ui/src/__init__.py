from .consts import API_URL, SEARCH_URL
from .api_client import ApiClient

client = ApiClient(API_URL)
search_client = ApiClient(SEARCH_URL)
