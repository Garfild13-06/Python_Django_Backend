import json
import os
import time
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models',
                                headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024, style=3):

        styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]

        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "styles": styles[style],
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run',
                                 headers=self.AUTH_HEADERS, files=data)
        print(response)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' +
                                    request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    api = Text2ImageAPI(
        os.getenv('FUSSIONBRAIN_API_URL'),
        os.getenv('FUSSIONBRAIN_API_KEY'),
        os.getenv('FUSSIONBRAIN_SECRET_KEY')
    )
    model_id = api.get_model()
    uuid = api.generate("Sun in sky", model_id)
    images = api.check_generation(uuid)

    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open("image.jpg", "wb") as file:
        file.write(image_data)
