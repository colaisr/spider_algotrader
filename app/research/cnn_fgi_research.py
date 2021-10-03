import json
import os
import requests


def get_cnn_fgi_rate():
    print('Getting an FGI index for today:')
    url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
    rk = os.environ.get('RAPIDAPI_KEY')
    headers = {
        'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com",
        'x-rapidapi-key': rk
        }

    response = requests.request("GET", url, headers=headers)
    rj=json.loads(response.text)
    val=rj['fgi']['now']['value']
    valtext=rj['fgi']['now']['valueText']
    print(response.text)
    return val,valtext

if __name__ == '__main__':
    get_cnn_fgi_rate()