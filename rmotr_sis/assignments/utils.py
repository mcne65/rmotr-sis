import requests


def run_code(code):
    url = "https://compile-g.remoteinterview.io/compile"
    resp = requests.post(url, data={"language": 0, "stdin": "", "code": code})
    return resp.json()
