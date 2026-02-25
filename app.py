from flask import Flask, request, jsonify, abort

from storage import FileConfigStorage

app = Flask(__name__)
repo = FileConfigStorage(base_path='data')


@app.get('/')
def index():
    return health()


@app.get('/health')
def health():
    return {"status": "UP"}


@app.get('/configs/<service>/<environment>')
def get_config(service, environment):
    version = request.args.get('version')
    config = repo.get(service, environment, version)
    if not config:
        abort(404)
    return jsonify(config)


@app.post('/configs/<service>/<environment>')
def save_config(service, environment):
    raise NotImplementedError(f'POST(Config: {service}-{environment})')


@app.get('/configs/<service>/<environment>/versions')
def list_versions(service, environment):
    versions = repo.list_versions(service, environment)
    return {
        'service': service,
        'environment': environment,
        'versions': versions
    }


if __name__ == '__main__':
    app.run(debug=True)
