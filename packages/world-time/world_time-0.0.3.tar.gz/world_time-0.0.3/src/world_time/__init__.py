import requests

URL = 'http://worldtimeapi.org/api/ip/'


def get_time_by_ip(ip):
    result = requests.get(URL + ip)
    return result.json()