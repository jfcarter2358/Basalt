import os
import json
import uuid
import flask
from flask import Response, request, redirect
from pprint import pprint
from cartils.logger import Logger

logger = Logger('DEBUG')
logger.INFO("Initializing server...")
app = flask.Flask(__name__, static_folder='../web/static', static_url_path='/static')
app.config["DEBUG"] = True

# UI

@app.route('/', methods=['GET'])
def index():
    return redirect("/ui/home")

@app.route('/ui/home', methods=['GET'])
def ui_home():
    template_file = 'web/templates/home.html'
    with open(template_file) as f:
        contents = f.read()
    return contents

# NETWORK API

# get all available networks
@app.route('/api/network/<project>/network', methods=['GET'])
def network_all(project):
    try:
        files = [f for f in os.listdir(f'data/projects/{project}/networks')]
        networks = {}
        for fi in files:
            uid = fi[:-5]
            with open(f'data/projects/{project}/networks/{fi}') as f:
                networks[uid] = json.load(f)
        return networks, 200
    except Exception as e:
        logger.ERROR(e)
        return Response(status=500)

# get a network
@app.route('/api/network/<project>/network/<uid>', methods=['GET'])
def newtork_get(project, uid):
    try:
        with open(f'data/projects/{project}/networks/{uid}.json')  as f:
            data = json.load(f)
        return data, 200
    except Exception as e:
        logger.ERROR(e)
        return Response(status=500)

# create a new blank network
@app.route('/api/network/<project>/network', methods=['POST'])
def network_post(project):
    try:
        name = request.args.get('name')
        description = request.args.get('description')
        data = {
            'name': name,
            'description': description,
            'nodes': [],
            'links': []
        }
        uid = str(uuid.uuid4())
        with open(f'data/projects/{project}/networks/{uid}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return {'uid': uid}, 200
    except Exception as e:
        logger.ERROR(e)
        return Response(status=500)

# update a network
@app.route('/api/network/<project>/network/<uid>', methods=['PUT'])
def network_put(project, uid):
    try:
        data = request.json
        if not data:
            data = {}
            for el in request.form:
                data[el] = request.form.get(el)
        with open(f'data/projects/{project}/networks/{uid}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return Response(status=200)
    except Exception as e:
        logger.ERROR(e)
        return Response(status=500)

@app.route('/api/network/<project>/network/<uid>', methods=['DELETE'])
def user_delete(project, uid):
    try:
        os.remove(f'data/projects/{project}/networks/{uid}.json')
        return Response(status=200)
    except Exception as e:
        logger.ERROR(e)
        return Response(status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    