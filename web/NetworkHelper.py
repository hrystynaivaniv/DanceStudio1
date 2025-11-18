import requests
from requests.auth import HTTPBasicAuth

class NetworkHelper:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password) if username and password else None

    def get_list(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}/", auth=self.auth)
        return response.json() if response.ok else []

    def get(self, _id, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}/{_id}/", auth=self.auth)
        return response.json() if response.ok else None

    def create(self, data, endpoint):
        response = requests.post(f"{self.base_url}/{endpoint}/", json=data, auth=self.auth)
        return response.json() if response.ok else None

    def update(self, _id, data, endpoint):
        response = requests.put(f"{self.base_url}/{endpoint}/{_id}/", json=data, auth=self.auth)
        return response.json() if response.ok else None

    def delete(self, _id, endpoint):
        response = requests.delete(f"{self.base_url}/{endpoint}/{_id}/", auth=self.auth)
        return response.status_code == 204
