from flask import Flask, jsonify
from flask import request
from flask import abort
from flask import make_response
from flask_cors import CORS

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = Flask(__name__)
cors = CORS(app, resources={r"/items/*": {"origins": "*"}})

def connect_database(server, port, database_name):
    result = None
    try:
        client = MongoClient(server, port)
        result = client[database_name]

        # test server is up.
        client.server_info()
    except ServerSelectionTimeoutError as exp:
        result = None
        print("No connection %s" % exp)
    return result


@app.errorhandler(404)
def not_found(error):
    """ Handler 404 error in a better way """
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_item(item):
    return {'name': item['name'], 'acitivity': item['activity']}


def get_items_from_database(name):
    # get a database connection
    db = connect_database(server="mongo",
                          port=27017,
                          database_name='catalog')

    items = []
    search_field = {"name": name}

    try:
        for item in db['visualise_data'].find(search_field):
            items.append(make_public_item(item))

    except AttributeError as exp:
        items = {'error': 'AttributeError: %s' % exp}

    return items


@app.route('/items', methods=['GET'])
def get_items():
    """
    Use GET method to get items for a specific subreddit provided by request.
    Use window time frame to get items.
    """
    name = request.args.get('name')

    if name is None:
        abort(400)

    items = get_items_from_database(name)

    return jsonify(items)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
