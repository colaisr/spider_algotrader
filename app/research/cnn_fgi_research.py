import json
import os
import requests


def get_cnn_fgi_rate():
    print('Getting an FGI index for today:')
    try:
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
    except Exception as e:
        print('problem with getting: ', e)
        return None,None

if __name__ == '__main__':
    get_cnn_fgi_rate()