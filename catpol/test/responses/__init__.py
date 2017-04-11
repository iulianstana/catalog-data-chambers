import os
import json
import pickle

class FrozenResponses:

    @staticmethod
    def __directory():
        d = 'catpol/test/responses/frozen/'
        snapshot_name = os.path.join(d, '{}/{}/{}/'.format(
            spider,
            method,
            url_filename))
        return d

    @staticmethod
    def __freeze(obj, fpath, fname):
        d = FrozenResponses.__directory()
        snapshot_fpath = os.path.join(d, fpath)
        snapshot_fname = os.path.join(snapshot_fpath, fname)

        if not os.path.exists(os.path.dirname(snapshot_fpath)):
            try:
                os.makedirs(os.path.dirname(snapshot_fpath))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(
            snapshot_fname, 'wb'
        ) as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def responses():
        d = 'catpol/test/responses/frozen'
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
