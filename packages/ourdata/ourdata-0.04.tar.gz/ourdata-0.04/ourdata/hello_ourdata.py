import requests

def hello_data():
    print("Hello Data!")
    print("Hello Data Again!")

def test_request():
    print(requests.get("https://rickandmortyapi.com/api/character/?page=2"))
