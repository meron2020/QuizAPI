import requests


def get_quiz(url):
    headers = {"content-type": "application/json", "connection": "keep-alive"}
    print(requests.get(url + "scoring", headers=headers).json())


get_quiz("http://127.0.0.1:5000/")