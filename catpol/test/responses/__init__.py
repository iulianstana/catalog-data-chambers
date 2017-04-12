import os
import json
import pickle

class FrozenResponses:

    @staticmethod
    def _root():
        return 'catpol/test/responses/frozen/'

    @staticmethod
    def _directory(url, spider, method):
        d = FrozenResponses._root()
        url_dir = url[url.find('//') + 2:].replace('/', '-')
        snapshot_name = os.path.join(d, spider, method, url_dir)
        return snapshot_name

    @staticmethod
    def _freeze(obj, fpath, fname):
        complete_path = os.path.join(fpath, fname)
        if not os.path.exists(os.path.dirname(complete_path)):
            try:
                os.makedirs(os.path.dirname(complete_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(
            complete_path, 'wb'
        ) as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def frozen_responses():
        d = FrozenResponses._root()
        for root, dirs, files in os.walk(d):
            if root.count('/') == d.count('/') + 3:
                d_response = os.path.join(root, 'response.pkl')
                response = pickle.load(open(d_response, 'rb'))

                d_results = os.path.join(root, 'results.pkl')
                results = pickle.load(open(d_results, 'rb'))

                spider = root.split('/')[-3]
                method = root.split('/')[-2]

                yield {
                    'response': response,
                    'results': results,
                    'spider': spider,
                    'method': method
                }

    @staticmethod
    def freeze_response(response, url, spider, method):
        frozen_dir = FrozenResponses._directory(url, spider, method)
        FrozenResponses._freeze(response, frozen_dir, 'response.pkl')

    @staticmethod
    def freeze_results(results, url, spider, method):
        frozen_dir = FrozenResponses._directory(url, spider, method)
        FrozenResponses._freeze(results, frozen_dir, 'results.pkl')
