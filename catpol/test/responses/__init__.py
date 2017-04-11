import os
import json
import pickle

class FrozenResponses:
    @staticmethod
    def responses():
        d = 'catpol/test/responses/frozen/'
        for f in os.listdir(d):
            if f.endswith(".pkl"):
                file_name = f[:-4]
                file_name_json = os.path.join(d, '{}.json'.format(file_name))
                file_name_pickle = os.path.join(d, '{}.pkl'.format(file_name))
                spider, method, timestamp = file_name.split('-')
                response = pickle.load(open(file_name_pickle, 'rb'))
                with open(file_name_json) as f:
                    result = json.load(f)
                yield {
                    'response': response,
                    'result': result,
                    'spider': spider,
                    'method': method
                }
