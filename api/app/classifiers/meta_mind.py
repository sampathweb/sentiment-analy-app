import json
import requests


class MetaMindTextClassifier(object):
    ''''Provides access to Metamind Prediction API for Text Classification'''

    API_URL = 'https://www.metamind.io/language/test'

    def __init__(self, auth_key, model_id):
        self.model_id = model_id
        self.credentials = ('Basic', auth_key)

    def predict(self, text):
        params = {}
        params['trained_model_id'] = self.model_id
        params['value'] = text
        resp = requests.get(self.API_URL, auth=self.credentials, params=params)
        if resp.status_code == requests.codes.ok:
            result = json.loads(resp.content)
            return result['prediction']
        return None
